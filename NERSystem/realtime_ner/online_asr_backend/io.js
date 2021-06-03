const sio = require('socket.io')

const io = sio()

io.on('connection', (socket) => {
  console.log('a user connected')

  socket.on('join room', data => {
    console.log('user joined room')
    socket.join(data.room)
  })
})

module.exports = io
