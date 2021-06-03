import React, { Component, createRef } from "react";
import styled from "styled-components";
import { withStyles } from "@material-ui/core/styles";
import { format } from "date-fns";

import { Flex, Box } from "@rebass/grid";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import Paper from "@material-ui/core/Paper";
import Input from "@material-ui/core/Input";
import Button from "@material-ui/core/Button";
import InputAdornment from "@material-ui/core/InputAdornment";
import IconButton from "@material-ui/core/IconButton";
import ClearRounded from "@material-ui/icons/ClearRounded";
import RootRef from "@material-ui/core/RootRef";
import FormControl from "@material-ui/core/FormControl";
import InputLabel from "@material-ui/core/InputLabel";
import Select from "@material-ui/core/Select";
import MenuItem from "@material-ui/core/MenuItem";
import TextField from "@material-ui/core/TextField";
import MicIcon from '@material-ui/icons/Mic';
import ClearAllIcon from '@material-ui/icons/ClearAll';
import FlightTakeoffIcon from '@material-ui/icons/FlightTakeoff';
import FlightIcon from '@material-ui/icons/Flight';
import MarkupText from "../modules/components/MarkupText";
import Switch from "@material-ui/core/Switch";

import io from 'socket.io-client';
import Record from './Record';
import Import from './Import';
const CHOICES=["AIR TRAFFIC","LOCATION"]

const EXAMPLES = [
  "singapore four six two zero hwa chong"
];

import nerData from '../data.json';

// Styles definition

const styles = theme => ({
  main: {
    padding: 20
  },
  paper: {
    flexGrow: 1,
    padding: "12px",
    display: "flex",
    alignItems: "center",
    justifyContent: "flex-start"
  },
  errorIcon: {
    fontSize: 20,
    marginRight: theme.spacing.unit
  },
  snackbarMessage: {
    display: "flex",
    alignItems: "center"
  }
});

const PaperFlex = styled(Flex)`
  height: 240px;
`;

const LogPaper = styled(Paper)`
  flex-grow: 1;
  flex-shrink: 1;
  flex-basis: 100%;
  min-width: 0;
  min-height: 0;
  overflow-y: scroll;
  padding: 8px;
  max-height: 240px;
  max-width: 100%;
`;

const LogEntry = styled.span`
  display: block;
`;

const ControlButton = styled(Button)`
  margin-right: 8px;
`;

// Functions definition

const getCurrentTimeString = () => format(new Date(), "HH:mm:ss");

class Transcription {
  index = 0;
  list = [];

  add = (text, isFinal) => {
    this.list[this.index] = text;
    if (isFinal) {
      this.index++;
    }
  };

  toString = () => {
    return this.list.join(". ");
  };

  clear = () => {
    this.index = 0;
    this.list = [];
  };
}

const debounce = (func, delay) => {
  let inDebounce;
  return function() {
    const context = this;
    const args = arguments;
    clearTimeout(inDebounce);
    inDebounce = setTimeout(() => func.apply(context, args), delay);
  };
};

class App extends Component {
//this.setState('backendUrl', 'http://localhost:3001')
  constructor(props) {
    super(props);
    this._sendWsMessage = debounce(this._sendWsMessage, 250);
    this.state = {
      text: "",
      output: "",
      highlight: [],
      choiceValue: "",
      errorVisible: false,
      exampleValue: "",
      mode: 'record',
      backendUrl: 'ws://localhost:5001',
      isSocketReady: false,
      transcription: '',
      partialResult: '',
      savedSocket:'null',
      status: 0, // 0: idle, 1: streaming, 2: finish
      isBusy: false,
      socket: null,
      switchstate: false,
      examples: []
    };
    this.handleSwitch = this.handleSwitch.bind(this);
    this.handleSpeechAreaChange = this.handleSpeechAreaChange.bind(this);
  }
  

  componentDidMount() {
    console.log(nerData);
    this.transcription = new Transcription();
    this._handleConnectWs();
    
    const socket = io(this.state.backendUrl, {
      reconnection: false,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: Infinity
    })
    this.setState({
     socket:socket
  })
    
   this.initSockets();
  }
 
  componentDidUpdate(prevProps, prevState) {
  if (prevState.backendUrl !== this.state.backendUrl) {
    this.ws.close();
    setTimeout(this._handleRetryWs, 1000);
  }
}

  initSockets () {
    console.log(this.state.backendUrl);
    this.state.socket = io(this.state.backendUrl, {
      reconnection: false,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: Infinity
    })

    this.state.socket.on('connect', () => {
      console.log('socket connected!')
    })

    this.state.socket.on('stream-ready', () => {
      this.setState({
        isSocketReady: true,
        status: 1
      })
    })

    this.state.socket.on('stream-data', data => {
      if (data.type === 'import') {
        if (data.status === 0 && data.message === 'EXIT') {
          this.setState({
            status: 2,
            isBusy: false
          })
        } else {
          this.setState({
            transcription: data.message
          })
	  this.handleSpeechAreaChange()
        }
      } else {
        if (data.result.final) {
          this.setState(prevState => ({
            transcription: prevState.transcription + ' ' + data.result.hypotheses[0].transcript,
            partialResult: ''
          }))
          this.handleSpeechAreaChange()
        } else {
          this.setState(prevState => ({
            partialResult: '[...' + data.result.hypotheses[0].transcript + ']'
          }))
        }
      }
    })
  
  this.state.socket.on('stream-close', () => {
  
  
      this.setState({
        status: 2,
        isBusy: false
      })
    })
    
  }

  onTokenChange = (e) => {
    this.setState({
      token: e.target.value
    })
  }

  reset = () => {
    this.setState({
      transcription: '',
      partialResult: ''
    })
  }

  setBusy = () => {
    this.setState({
      isBusy: true
    })
  }

  setStatus = (status) => {
    this.setState({
      status
    })
  }

  changeTab = (tab) => {
    if (this.state.isBusy) {
      const cf = window.confirm('If you change tab, current stream process will be lost')

      if (cf) {
        this.setState({
          mode: tab,
          isBusy: false
        })
        this.reset()
      }
    } else {
      this.setState({
        mode: tab
      })
      this.reset()
    }
  }
   

  logRef = createRef();

  _onWsMessage = e => {
    this.setState({ output: e.data });
  };

  _handleRetryWs = () => {
    this.setState({ errorVisible: false });
    this._handleConnectWs();
  };

  _handleConnectWs = () => {
    console.log("socket connecting to " + this.state.backendUrl);
    this.ws = new WebSocket(this.state.backendUrl);
    this.ws.onopen = () => console.log("connected to ws");
    this.ws.onclose = () => {
      console.log("socket disconnected");
      this.setState({ errorVisible: true });
    }
    this.ws.onmessage = this._onWsMessage;
  };

  componentWillUnmount() {
    if (this.ws) {
      this.ws.close();
    }
  }

 handleSpeechAreaChange(){
    let transcribedValue = this.state.transcription
    this.setState({text: transcribedValue})
  };

  _handleTextAreaChange = e => {
    this.setState({ text: e.target.value });
  };
  
  _handleSpeechChange = e => {
    this.setState({ transcription:  e.target.value });
  };
  
  _clearInput = () => {
    this.setState({ text: "" });
  };

  handleSwitch(e){
    e.preventDefault();
    let name = e.target.name;
    this.setState({[name]:e.target.checked})
  }

  shouldComponentUpdate(_, nextState) {
    if (nextState.text !== this.state.text) {
      this._sendWsMessage(nextState.text);
    }
    return true;
  }

  _sendWsMessage = message => {
    this.ws.send(message);
  };

  _handleExampleChange = e => {
    if (e.target.value === "") {
      this.setState({
        exampleValue: ""
      });
    } else {
      this.setState({
        text: this.state.examples[e.target.value],
        exampleValue: e.target.value
      });
    }
  };

_handleChoiceChange = e => {
    if (e.target.value === "") {
      this.setState({
        choiceValue: ""
      });
    } else {
	  this.choiceChoosen=nerData[e.target.value]

      this.setState({

      });
      console.log(this.choiceChoosen + "cpress the emergency button");

      console.log(nerData, e.target.value);
      this.setState({
        choiceValue: e.target.value,
        "backendUrl": nerData[e.target.value]["ner_ws_endpoint"],
        "examples": nerData[e.target.value]["examples"]
      })

    }
  };
  render() {
    const { classes } = this.props;
    const {
      text,
      errorVisible,
      output,
      exampleValue,
      choiceValue
    } = this.state;
    return (
      <>
        <AppBar position="static" style={{ background: '#3FA6EF' }}>
          <Toolbar>
            <Typography variant="h6" color="default">
              <InputLabel htmlFor="choice-select">
                  Select a NER 
                </InputLabel>
                
                <Select
                  value={choiceValue}
                  onChange={this._handleChoiceChange}
                  inputProps={{ id: "choice-select" }}
                  autoWidth
                >
                <MenuItem value="AIR TRAFFIC">
                    <em>NONE</em>
                  </MenuItem>
                  {nerData.map(({ner_name: choice}, idx) => (
                    <MenuItem value={idx} key={idx}>
                      {choice}
                    </MenuItem>
                  ))}
                </Select>
            </Typography>
	    
          </Toolbar>
        </AppBar>
        <Box p={3}>
          <Flex flexWrap="wrap" mb={2}>
            <PaperFlex flexDirection="column" width={[1, 1 / 2]} pr={[0, 2]}>
              <Typography variant="h6">Input text</Typography>
              <Paper className={classes.paper}>
		{/*{this.state.switchstate === false && */}
                <Input
                  multiline
                  fullWidth
                  placeholder="Type here..."
                  onChange={this._handleTextAreaChange }
                  value={text}
                  endAdornment={
                    <InputAdornment position="end">
                      <IconButton onClick={this._clearInput}>
                        <ClearRounded />
                      </IconButton>
                    </InputAdornment>
            	}
                />
		{/*}
                {
		{this.state.switchstate &&
		<textarea
                value={this.state.transcription + ' ' + this.state.partialResult}
                readOnly
                className={`form-control ${this.state.status === 2 ? 'success' : ''}`}
                rows="8"
                cols="80"
                />
		} */}

              </Paper>
	{/*	<Switch
			checked={this.state.switchstate}
			onChange={this.handleSwitch}
			value="checkedA"
			name="switchstate"
			inputProps={{'aria-label':'secondary checkbox'}}
		/> */}
            </PaperFlex>
            <PaperFlex flexDirection="column" width={[1, 1 / 2]} pl={[0, 2]}>
              <Typography variant="h6">Results</Typography>
              <Paper className={classes.paper}>
                <MarkupText text={output} />
              </Paper>
            </PaperFlex>
          </Flex>
            {/*change ner*/}
              	
                {/*cend of change ner*/}
          <Flex flexDirection="column">
            <Flex alignItems="center" py={1}>
              <FormControl fullWidth>
            
                <InputLabel htmlFor="example-select">
                  Select an example
                </InputLabel>
                
                <Select
                  value={exampleValue}
                  onChange={this._handleExampleChange}
                  inputProps={{ id: "example-select" }}
                  autoWidth
                >
                  <MenuItem value="">
                    <em>None</em>
                  </MenuItem>
                  {this.state.examples.map((example, idx) => (
                    <MenuItem value={idx} key={idx}>
                      {example}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Flex>
            <Flex alignItems="center" py={1}>
              <Typography variant="subtitle1">
                Highlighter server status:{" "}
                <strong>{choiceValue === "" ? "Highlighter unavailable. Choose an NER from top left" : errorVisible ? "Disconnected" : "Connected"}</strong>
              </Typography>
              {errorVisible && (
                <Button color="secondary" onClick={this._handleRetryWs}>
                  Retry
                </Button>
              )}
            
            </Flex>

            <Flex alignItems="center" flexWrap="wrap" py={1}>
              <Box width={[1]} pr={[0, 2]}>
                <TextField
                  label="Token"
                  value={this.state.asrUrl}
                  onChange={this.onTokenChange}
                  fullWidth
                />
              </Box>
            </Flex>
           <br></br>
              <Flex alignItems="center" flexWrap="wrap" py={1}>
              <Box width="true">
                <button onClick={() => this.changeTab('record')} className={`btn btn-tab nav-link ${this.state.mode === 'record' ? 'active' : ''}`} >
                  Recording
                </button>
		 </Box>
		<Box width={[1, 1 / 2]} pl={[0, 2]}>
                <button onClick={() => this.changeTab('import')} className={`btn btn-tab nav-link ${this.state.mode === 'import' ? 'active' : ''}`} >
                  Import audio
                </button>
            	</Box>
		</Flex>

	<br></br>


           <div>
              {
                this.state.mode === 'record' ? 
                <Record
                  socket={this.state.socket}
                  isBusy={this.state.isBusy}
                  token={this.state.token}
                  isSocketReady={this.state.isSocketReady}
                  backendUrl={this.state.backendUrl}
                  reset={this.reset}
                  setBusy={this.setBusy}
                /> : <Import
                  backendUrl={this.state.backendUrl}
                  token={this.state.token}
                  setBusy={this.setBusy}
                  socket={this.state.socket}
                  setStatus={this.setStatus}
                />
              }
            </div>
            <div
              className="form-group transcription"
            >
              <span
                className="is-finish"
              >
                <i className="fal fa-check" />
              </span>
              {/*<textarea
                value={this.state.transcription + ' ' + this.state.partialResult}
                readOnly
                className={`form-control ${this.state.status === 2 ? 'success' : ''}`}
                rows="8"
                cols="80"
              />*/}
            </div>
           
          </Flex>
        </Box>
      </>
    );
  }
}

export default withStyles(styles)(App);

