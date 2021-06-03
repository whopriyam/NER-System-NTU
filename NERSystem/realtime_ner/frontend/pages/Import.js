import React, { Component } from 'react'
import axios from 'axios'

export default class Import extends Component {
  constructor (props) {
    super(props)

    this.state = {
      filename: ''
    }
  }
  
  componentDidMount() {
    this.props.setStatus(0)
  }
  

  onFileChange = async (e) => {
    this.setState({
      filename: e.target.files[0].name
    })

    const formData = new FormData()
    formData.append('file', e.target.files[0])
    formData.append('token', this.props.token)

    await axios.post(`${this.props.backendUrl}/stream/import`, formData)

    this.props.setBusy()
  }

  componentWillUnmount() {
    this.props.socket.emit('stream-cancel')
  }
  

  render () {
    return (
      <div className="row mt-5">
        <div className="col-md-12">
          <div className="input-group mb-3">
            <div className="custom-file">
              <input type="file" className="custom-file-input" id="inputGroupFile02" onChange={this.onFileChange} />
              <label className="custom-file-label" htmlFor="inputGroupFile02" aria-describedby="inputGroupFileAddon02">
            {/*    {
                  this.state.filename.length ? this.state.filename : 'Choose file'
                } */}
              </label>
            </div>
            <div className="input-group-append">
              {/*<span className="input-group-text" id="inputGroupFileAddon02">Upload</span> */}
            </div>
          </div>
        </div>
      </div>
    )
  }
}
