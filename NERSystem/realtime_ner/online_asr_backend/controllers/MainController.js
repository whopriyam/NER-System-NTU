const WebSocketClient = require('websocket').client
const io = require('../io')
const spawn = require('child_process').spawn
const fs = require('fs')

const englishOnlineServerUrl = 'ws://40.90.170.182:8001/client/ws/speech' // this is address for english model, change it to your target model (malay, chinese,...)

class MainController {
  static async streamByRecording (req, res, next) {
    try {
      const token = req.body.token

      let client = new WebSocketClient()
      let conn = null
      client.on('connectFailed', (error) => {
        console.log('Connect Error: ' + error.toString())
        io.emit('stream-close') // send close signal to client
      })

      client.on('connect', (connection) => {
        conn = connection
        console.log('WebSocket Client Connected')

        io.emit('stream-ready') // tell frontend that socket is ready

        connection.on('error', (error) => {
          console.log('Connection Error: ' + error.toString())
        })
        connection.on('close', () => {
          console.log('echo-protocol Connection Closed')

          io.emit('stream-close') // send close signal to client

          client = null
        })
        connection.on('message', (message) => {
          const data = JSON.parse(message.utf8Data)

          if (data.status === 0 && data.result) { // only send data which is truely a transcription to browser
            io.emit('stream-data', data)
          }
        })
      })

      // start connect to online server
      client.connect(`${englishOnlineServerUrl}?content-type=audio/x-raw,+layout=(string)interleaved,+rate=(int)16000,+format=(string)S16LE,+channels=(int)1?token=${token}`, null, null, null, null)

      // in this example, client doesn't join any room. so in here we need to listen on all sockets connected to backend
      Object.keys(io.sockets.connected).forEach(key => {
        io.sockets.connected[key].on('stream-input', data => {
          if (conn) {
            conn.sendBytes(data)
          }
        })

        io.sockets.connected[key].on('stream-stop', data => {
          if (conn) {
            conn.sendBytes(data) // send remained data in buffer before closing
            conn.sendUTF('EOS') // after this conn.close() will be called because server will stop the connection
          }
        })

        io.sockets.connected[key].on('stream-cancel', () => {
          conn.close() // immediately close connection to online server
        })
      })

      return res.json({
        success: true
      })
    } catch (e) {
      return res.status(500).json({
        message: 'Error when streaming'
      })
    }
  }

  static async streamByImport (req, res, next) {
    try {
      const token = req.body.token

      const ls = spawn('python', ['client_2.py', '-u', englishOnlineServerUrl, '-r', '32000', '-t', token, req.file.path])
      ls.stdout.on('data', (data) => {
        // print at the final of ASR
        // we don't actually need this event
      })
      ls.stderr.on('data', (data) => { // print during ASR
        io.emit('stream-data', {
          type: 'import',
          message: data.toString(),
          status: 1
        })
      })
      ls.on('exit', async (code) => {
        if (fs.existsSync(req.file.path)) { // clean file after streaming
          fs.unlinkSync(req.file.path)
        }

        io.emit('stream-data', { // send close message to browser
          type: 'import',
          message: 'EXIT',
          status: 0 // tell browser it finished ASR
        })
      })

      Object.keys(io.sockets.connected).forEach(key => {
        // if user manually cancel (by changing tab, close browser)
        // then we terminate the child process
        io.sockets.connected[key].on('stream-cancel', () => {
          ls.kill()
        })
      })

      return res.json({
        success: true
      })
    } catch (e) {
      return res.status(500).json({
        message: 'Error when streaming'
      })
    }
  }
}

module.exports = MainController
