import React, { Component } from 'react'
import './recorder'
import axios from 'axios'

export default class Record extends Component {
  constructor (props) {
    super(props)
    this.state = {
      recorder: {},
      recordInterval: 0
    }
  }

  async componentDidMount () {
    await this.prepare()

    this.props.socket.on('stream-close', () => {
     this.cancel()
    })
  }

  componentWillUnmount() {
    // cancel recorder from browser
    window.cancelAnimationFrame(this.drawVisual)
    const track = this.mediaStream.getTracks()[0]
    track.stop()

    this.cancel() // cancel stream
  }
  

  async prepare () {
    this.canvas = document.querySelector('.visualizer')
    this.canvasCtx = this.canvas.getContext('2d')
    const intendedWidth = document.querySelector('.visualizer-container').clientWidth
    this.canvas.setAttribute('width', 1203) //initial is intendedWidth
    this.canvas.setAttribute('height', 200)
    
    {/*
    if (intendedWidth / 2 < 500) {
      this.canvas.style.width = intendedWidth + 'px'
    } else {
      this.canvas.style.width = (intendedWidth / 2) + 'px'
    }
    */}
    this.canvas.style.height = '100px'  

    this.audioCtx = new (window.AudioContext || window.webkitAudioContext)()
    let source

    this.analyser = this.audioCtx.createAnalyser()
    this.analyser.minDecibels = -90
    this.analyser.maxDecibels = -10
    this.analyser.smoothingTimeConstant = 0.85

    const distortion = this.audioCtx.createWaveShaper()
    const gainNode = this.audioCtx.createGain()
    const biquadFilter = this.audioCtx.createBiquadFilter()
    const convolver = this.audioCtx.createConvolver()

    if (!navigator.mediaDevices) {
      console.log('browser doesn\'t support')
      // this.$emit('onError', 'Your browser doesn\'t support audio recorder. Make sure you grant permission for recording audio and your browser is running with HTTPS')
    }

    if (navigator.mediaDevices.getUserMedia) {
      console.log('getUserMedia supported.')
      const constraints = { audio: true }
      try {
        this.mediaStream = await navigator.mediaDevices.getUserMedia(constraints)

        source = this.audioCtx.createMediaStreamSource(this.mediaStream)
        this.audioStream = source
        // Firefox loses the audio input stream every five seconds
        // To fix added the input to window.source
        // window.source = source
        source.connect(distortion)
        distortion.connect(biquadFilter)
        biquadFilter.connect(gainNode)
        convolver.connect(gainNode)
        gainNode.connect(this.analyser)
        this.analyser.connect(this.audioCtx.destination)
        this.audioCtx.resume()
        this.visualize()

        // -------IMPORTANT------
        // eslint-disable-next-line no-undef
        const recorder = new Recorder(source, { workerPath: '/recorderWorker.js' })
        this.setState({
          recorder
        })
      } catch (e) {
        console.log('The following error occured: ' + e)
        // this.$emit('onError', e.toString())
      }
    } else {
      // this.$emit('onError', 'getUserMedia not supported on your browser!')
      console.log('getUserMedia not supported on your browser!')
    }
  }

  visualize () {
    this.analyser.fftSize = 2048
    this.bufferLength = this.analyser.fftSize
    this.dataArray = new Uint8Array(this.bufferLength)

    this.canvasCtx.clearRect(0, 0, this.canvas.width, this.canvas.height)

    this.draw()
  }

  draw = () => {
    this.drawVisual = requestAnimationFrame(this.draw)

    this.analyser.getByteTimeDomainData(this.dataArray)

    this.canvasCtx.fillStyle = '#f7fafc'
    this.canvasCtx.fillRect(0, 0, this.canvas.width, this.canvas.height)

    this.canvasCtx.lineWidth = 2
    this.canvasCtx.strokeStyle = '#007aff'

    this.canvasCtx.beginPath()

    const sliceWidth = this.canvas.width * 1.0 / this.bufferLength
    let x = 0

    for (let i = 0; i < this.bufferLength; i++) {
      const v = this.dataArray[i] / 128.0
      const y = v * this.canvas.height / 2

      if (i === 0) {
        this.canvasCtx.moveTo(x, y)
      } else {
        this.canvasCtx.lineTo(x, y)
      }

      x += sliceWidth
    }

    this.canvasCtx.lineTo(this.canvas.width, this.canvas.height / 2)
    this.canvasCtx.stroke()
  }

  // -------IMPORTANT------
  // Function below
  start = async () => {
    try {
      if (this.props.isBusy) {
        return
      }

      this.props.reset()
    
      await axios.post(`${this.props.backendUrl}/stream/record`, {
        token: this.props.token
      })


      const recordInterval = setInterval(() => {
        this.state.recorder.export16kMono((blob) => {
          if (this.props.isSocketReady) {
            this.props.socket.emit('stream-input', blob)
          }
          this.state.recorder.clear()
        }, 'audio/x-raw')
      }, 250)

      this.setState({
        recordInterval
      })

      // Start recording
      this.state.recorder.record()

      this.props.setBusy()
    } catch (err) {
      console.log(err)
    }
  }

  // -------IMPORTANT------
  // Function below
  stop = () => {
    clearInterval(this.state.recordInterval)
    // Stop recording
    if (this.state.recorder) {
      this.state.recorder.stop()
      // Push the remaining audio to the server
      this.state.recorder.export16kMono((blob) => {
        if (this.props.isSocketReady) {
          this.props.socket.emit('stream-stop', blob)
        }
        this.state.recorder.clear()
      }, 'audio/x-raw')
    } else {
      this.$emit('onError', 'Recorder undefined')
    }
  }
  
  // -------IMPORTANT------
  // Function below
  cancel = () => {
    // Stop the regular sending of audio (if present)
    clearInterval(this.state.recordInterval)
    if (this.state.recorder) {
      this.state.recorder.stop()
      this.state.recorder.clear()
      if (this.props.isSocketReady) {
        this.props.socket.emit('stream-cancel')
      }
    }
  }

  render () {
    return (
      <div className="row">
        <div className="col-md-12 mt-5">
          <div className="visualizer-container">
            <canvas className="visualizer" />
          </div>
        </div>
        <div className="col-md-12 mt-3">
          <div className="row">
            <div className="col-md-12">
              <div className="controls text-center mb-3">
                <div
                  className="btn-group"
                  role="group"
                  aria-label="Basic example"
                >
                  <button
                    type="button"
                    className="btn btn-primary"
                    title="Starts listening for speech, i.e. starts recording and transcribing."
                    onClick={this.start}
                  >
                    <i className="fas fa-play" />
                    Start
                  </button>
                  <button
                    type="button"
                    title="Stops listening for speech. Speech captured so far will be recognized as if the user had stopped speaking at this point. Note that in the default case, this does not need to be called, as the speech endpointer will automatically stop the recognizer listening when it determines speech has completed."
                    className="btn btn-danger"
                    onClick={this.stop}
                  >
                    <i className="fas fa-stop" />
                    Stop
                  </button>
                  <button
                    type="button"
                    className="btn btn-warning"
                    title="Cancels the speech recognition."
                    onClick={this.cancel}
                  >
                    <i className="fal fa-power-off" />
                    Cancel
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }
}
