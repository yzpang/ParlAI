/*
 * Copyright (c) 2017-present, Facebook, Inc.
 * All rights reserved.
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree. An additional grant
 * of patent rights can be found in the PATENTS file in the same directory.
 */

import React from 'react';
import { 
  Form,
  FormControl, 
  Button, 
  Radio,
  ControlLabel,
  FormGroup,
  FormLabel } from 'react-bootstrap';
import Slider from 'rc-slider';
import { getCorrectComponent } from "./core_components.jsx";
import $ from 'jquery';


class EvaluatorIdleResponse extends React.Component {
  render() {
    // TODO maybe move to CSS?
    let pane_style = {
      paddingLeft: '25px',
      paddingTop: '20px',
      paddingBottom: '20px',
      paddingRight: '25px',
      float: 'left',
    };

    return (
      <div
        id="response-type-idle"
        className="response-type-module"
        style={pane_style}
      >
        <span>
          The writers are composing their claims right now.
        </span>
      </div>
    );
  }
}

class WriterIdleResponse extends React.Component {
  render() {
    // TODO maybe move to CSS?
    let pane_style = {
      paddingLeft: '25px',
      paddingTop: '20px',
      paddingBottom: '20px',
      paddingRight: '25px',
      float: 'left',
    };

    return (
      <div
        id="response-type-idle"
        className="response-type-module"
        style={pane_style}
      >
        <span>
          The evaluators are ranking your claims right now.
        </span>
      </div>
    );
  }
}

class WriterResponse extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      entailText: '',
      contradictText: '',
      neutralText: '',
      taskData: [],
      sending: false};
    this.handleInputChange = this.handleInputChange.bind(this);
    // this.handleEnterKey = this.handleEnterKey.bind(this);
  }

  // constructor(props) {
  //   super(props);
  //   this.state = { 
  //     textval: '',
  //     entailText: '',
  //     contradictText: '',
  //     neutralText: '',
  //     sending: false };
  // }

  componentDidUpdate(prevProps, prevState, snapshot) {
    // Only change in the active status of this component should cause a
    // focus event. Not having this would make the focus occur on every
    // state update (including things like volume changes)
    if (this.props.active && !prevProps.active) {
      $('input#id_text_input').focus();
    }
    this.props.onInputResize();
  }

  tryMessageSend() {
    if (this.state.entailText != '' && this.state.contradictText != '' && this.state.neutralText != '' && this.props.active && !this.state.sending) {
      this.setState({ sending: true });
      this.props.onMessageSend(this.state.entailText, this.state.contradictText , this.state.neutralText, {}, () =>
        this.setState({ entailText: '', contradictText: '', neutralText: '', sending: false })
      );
    }
  }

  handleKeyPress(e) {
    if (e.key === 'Enter') {
      this.tryMessageSend();
      e.stopPropagation();
      e.nativeEvent.stopImmediatePropagation();
    }
  }

  // checkValidData() {
  //   console.log(this.state);
  //   if (this.state.entailText !== "") {
  //     let response_data = {
  //       entailText: this.state.entailText,
  //     };
  //     this.props.onValidDataChange(true, response_data);
  //     return;
  //   }
  //   this.props.onValidDataChange(false, {});
  // }

  // handleInputChange(event) {
  //   console.log(event);
  //   let target = event.target;
  //   let value = target.value;
  //   let name = target.name;

  //   this.setState({ [name]: value }, this.checkValidData);
  // }

  handleInputChange(event) {
    console.log(event)
    let target = event.target;
    let value = target.value;
    let name = target.name;

    this.setState({ [name]: value });
  }

  updateValue(amount) {
    if ((amount != '' && isNaN(amount)) || amount < 0) {
      return;
    }
    amount = amount == '' ? 0 : amount;
    this.setState({ entailText: '' + amount });
  }

  render() {
    // TODO maybe move to CSS?
    let pane_style = {
      paddingLeft: '25px',
      paddingTop: '20px',
      paddingBottom: '20px',
      paddingRight: '25px',
      float: 'left',
      width: '100%',
    };
    let input_style = {
      height: '50px',
      width: '100%',
      display: 'block',
      float: 'left',
    };
    let submit_style = {
      width: '100px',
      height: '100%',
      fontSize: '16px',
      float: 'left',
      marginLeft: '10px',
      padding: '0px',
    };

    let text_entail = (
      <div>
        Please write a claim that is <b> Definitely Correct </b> about the situation or event in the prompt.
      </div>
      );
    let entail_input = (
      <div>
        <ControlLabel>{text_entail}</ControlLabel>
        <FormControl
          type="text"
          id="id_text_input0"
          name="entailText"
          style={{
            width: '80%',
            height: '100%',
            float: 'left',
            fontSize: '16px',
          }}
          value={this.state.entailText}
          placeholder="Please enter you claim here..."
          onKeyPress={e => this.handleKeyPress(e)}
          onChange={this.handleInputChange}
          disabled={!this.props.active || this.state.sending}
        />
      </div>
    );

    // onChange={e => this.updateValue(e.target.value)}

    let text_contradict = (
      <div>
        Please write a claim that is <b> Definitely Incorrect </b> about the situation or event in the prompt.
      </div>
      );
    let contradict_input = (
      <div>
        <ControlLabel>{text_contradict}</ControlLabel>
        <FormControl
          type="text"
          id="id_text_input1"
          name="contradictText"
          style={{
            width: '80%',
            height: '100%',
            float: 'left',
            fontSize: '16px',
          }}
          value={this.state.contradictText}
          placeholder="Please enter you claim here..."
          onKeyPress={e => this.handleKeyPress(e)}
          onChange={this.handleInputChange}
          disabled={!this.props.active || this.state.sending}
        />
      </div>
    );

    let text_neutral = (
      <div>
        Please write a claim that is <b> Neither </b> definitely correct nor definitely incorrect about the situation or event in the prompt.
      </div>
      );
    let neutral_input = (
      <div>
        <ControlLabel>{text_neutral}</ControlLabel>
        <FormControl
          type="text"
          id="id_text_input2"
          name="neutralText"
          style={{
            width: '80%',
            height: '100%',
            float: 'left',
            fontSize: '16px',
          }}
          value={this.state.neutralText}
          placeholder="Please enter you claim here..."
          onKeyPress={e => this.handleKeyPress(e)}
          onChange={this.handleInputChange}
          disabled={!this.props.active || this.state.sending}
        />
      </div>
    );

    // let text_input = (
    //   <FormControl
    //     type="text"
    //     id="id_text_input"
    //     style={{
    //       width: '80%',
    //       height: '100%',
    //       float: 'left',
    //       fontSize: '16px',
    //     }}
    //     value={this.state.textval}
    //     placeholder="Please enter here..."
    //     onKeyPress={e => this.handleKeyPress(e)}
    //     onChange={e => this.updateValue(e.target.value)}
    //     disabled={!this.props.active || this.state.sending}
    //   />
    // );

    // let hypotheses = (
    //   <div>
    //     <Form>
    //       <FormGroup controlId="entailText">
    //         <FormLabel>Please write a claim that is <b> Definitely Correct </b> about the situation or event in the prompt.</FormLabel>
    //         <FormControl type="text" 
    //         placeholder="Please write your claim here..." 
    //         onChange={this.handleInputChange}/>
    //       </FormGroup>

    //       <FormGroup controlId="contradictText">
    //         <FormLabel>Please write a claim that is <b> Definitely Incorrect </b> about the situation or event in the prompt.</FormLabel>
    //         <FormControl type="text" 
    //         placeholder="Please write your claim here..." 
    //         onChange={this.handleInputChange}/>
    //       </FormGroup>
          
    //       <FormGroup controlId="neutralText">
    //         <FormLabel>Please write a claim that is <b> Neither </b> definitely correct nor definitely incorrect about the situation or event in the prompt.</FormLabel>
    //         <FormControl type="text" 
    //         placeholder="Please write your claim here..." 
    //         onChange={this.handleInputChange}/>
    //       </FormGroup>
    //     </Form>
    //   </div>
    // );

    // TODO attach send message callback
    let submit_button = (
      <Button
        className="btn btn-primary"
        style={submit_style}
        id="id_send_msg_button"
        disabled={
          this.state.entailText == '' || this.state.contradictText == '' || this.state.neutralText == '' || !this.props.active || this.state.sending
        }
        onClick={() => this.tryMessageSend()}
      >
        Send
      </Button>
    );

    return (
      <div
        id="response-type-text-input"
        className="response-type-module"
        style={pane_style}
      >
        <div style={input_style}>
        {entail_input}
        {contradict_input}
        {neutral_input}
        {submit_button}
        </div>
      </div>
    );
  }
}

class EvaluatorResponse extends React.Component {
  constructor(props) {
    super(props);
    this.state = { textval: '', sending: false };
  }

  tryMessageSend(value) {
    if (this.props.active && !this.state.sending) {
      this.setState({ sending: true });
      this.props.onMessageSend(value, {}, () =>
        this.setState({ textval: '', sending: false })
      );
    }
  }

  _showMessage = (bool) => {
    this.setState({
      showMessage: bool
    });
  }

  render() {
    // TODO maybe move to CSS?
    let pane_style = {
      paddingLeft: '25px',
      paddingTop: '20px',
      paddingBottom: '20px',
      paddingRight: '25px',
      float: 'left',
      width: '100%',
    };
    let input_style = {
      height: '50px',
      width: '100%',
      display: 'block',
      float: 'left',
    };
    let submit_style = {
      width: '100px',
      height: '100%',
      fontSize: '16px',
      float: 'left',
      marginLeft: '10px',
      padding: '0px',
    };

    let reject_button1 = (
      <Button
        className="btn btn-danger"
        style={submit_style}
        id="id_reject_claim1_button"
        disabled={!this.props.active || this.state.sending}
        onClick={this._showMessage.bind(null, false)}
      >
        Invalid
      </Button>
    );
    // onClick={() => this.tryMessageSend('invalid')}

    let approve_button1 = (
      <Button
        className="btn btn-success"
        style={submit_style}
        id="id_approve_claim1_button"
        disabled={!this.props.active || this.state.sending}
        onClick={this._showMessage.bind(null, false)}
      >
        Approve
      </Button>
    );
    //onClick={this._showMessage.bind(null, false)}

    let reject_button2 = (
      <Button
        className="btn btn-danger"
        style={submit_style}
        id="id_reject_claim1_button"
        disabled={!this.props.active || this.state.sending}
        onClick={this._showMessage.bind(null, true)}
      >
        Invalid
      </Button>
    );
    // onClick={() => this.tryMessageSend('invalid')}

    let approve_button2 = (
      <Button
        className="btn btn-success"
        style={submit_style}
        id="id_approve_claim1_button"
        disabled={!this.props.active || this.state.sending}
        onClick={this._showMessage.bind(null, true)}
      >
        Approve
      </Button>
    );
    //onClick={this._showMessage.bind(null, false)}

    let text_rank1 = "Which claim do you think is better?" ;
    let rank1 = (
      <div>
        <ControlLabel> {text_rank1} </ControlLabel>
        <FormGroup>
          <Radio
            name="groupOptions1"
          >
            Claim 1
          </Radio>
          <Radio
            name="groupOptions1"
          >
            Claim 2
          </Radio>
        </FormGroup>
      </div>
    );

    // // TODO: remove this in the 2 writer setting. redundant.
    // let text_rank2 = "Which claim do you think is worse?" ;
    // let rank2 = (
    //   <div>
    //     <ControlLabel> {text_rank2} </ControlLabel>
    //     <FormGroup>
    //       <Radio
    //         name="groupOptions2"
    //       >
    //         Claim 1
    //       </Radio>
    //       <Radio
    //         name="groupOptions2"
    //       >
    //         Claim 2
    //       </Radio>
    //     </FormGroup>
    //   </div>
    // );

    
    let text_reasoning =
      "Optionally, please provide a brief justification for your ranking";
    // TODO: test text box.
    let text_reason = (
      <div>
        <ControlLabel>{text_reasoning}</ControlLabel>
        <FormControl
          type="text"
          id="id_text_input"
          style={{
            width: '80%',
            height: '100%',
            float: 'left',
            fontSize: '16px',
          }}
          value={this.state.textval}
          placeholder="Optionally add explanation here..."
          onKeyPress={e => this.handleKeyPress(e)}
          onChange={e => this.updateValue(e.target.value)}
          disabled={!this.props.active || this.state.sending}
        />
      </div>
    );

    return (
      <div
        id="response-type-text-input"
        className="response-type-module"
        style={pane_style}
      >
        <div style={input_style}>
          <div>Claims 1: {approve_button1} {reject_button1}</div>
          <div>Claims 2: {approve_button2} {reject_button2}</div>
        </div>
        { this.state.showMessage && (<div style={input_style}>{rank1}</div>) }
        <div style={input_style}>
        {text_reason}
        </div>
        // <div style={input_style}>
        //   {rank1}
        // </div>
        // <div style={input_style}>
        //   {rank2}
        // </div>
      </div>
    );
  }
}

class ResponsePaneWriter extends React.Component {
  render() {
    let v_id = this.props.v_id;
    let XDoneResponse = getCorrectComponent("XDoneResponse", v_id);
    let XFormResponse = getCorrectComponent('XFormResponse', v_id);
    // let XWriterResponse = getCorrectComponent("XWriterResponse", v_id);

    // let response_pane = null;
    // switch (this.props.task_state) {
    //   case "done":
    //     response_pane = <XDoneResponse {...this.props} />;
    //     break;
    //   default:
    //     response_pane = <WriterResponse {...this.props} />;
    //     break;
    // }

    let response_pane = null;
    switch (this.props.chat_state) {
      case 'done':
      case 'inactive':
        response_pane = <XDoneResponse {...this.props} />;
        break;
      case 'text_input':
      case 'waiting':
        if (this.props.task_data && this.props.task_data['respond_with_form']) {
          response_pane = (
            <WriterResponse
              {...this.props}
              active={this.props.chat_state == 'text_input'}
            />
          );
        } else {
          response_pane = (
            <WriterResponse
              {...this.props}
              active={this.props.chat_state == 'text_input'}
            />
          );
        }
        break;
      case 'idle':
      default:
        response_pane = <WriterIdleResponse {...this.props} />;
        break;
    }

    return (
      <div
        id="right-bottom-pane"
        style={{ width: "100%", backgroundColor: "#eee" }}
      >
        {response_pane}
      </div>
    );
  }
}

class ResponsePaneyEvaluator extends React.Component {
  render() {
    let v_id = this.props.v_id;
    let XDoneResponse = getCorrectComponent("XDoneResponse", v_id);
    let XFormResponse = getCorrectComponent('XFormResponse', v_id);
    // let XWriterResponse = getCorrectComponent("XWriterResponse", v_id);

    // let response_pane = null;
    // switch (this.props.task_state) {
    //   case "done":
    //     response_pane = <XDoneResponse {...this.props} />;
    //     break;
    //   default:
    //     response_pane = <WriterResponse {...this.props} />;
    //     break;
    // }

    let response_pane = null;
    switch (this.props.chat_state) {
      case 'done':
      case 'inactive':
        response_pane = <XDoneResponse {...this.props} />;
        break;
      case 'text_input':
      case 'waiting':
        if (this.props.task_data && this.props.task_data['respond_with_form']) {
          response_pane = (
            <EvaluatorResponse
              {...this.props}
              active={this.props.chat_state == 'text_input'}
            />
          );
        } else {
          response_pane = (
            <EvaluatorResponse
              {...this.props}
              active={this.props.chat_state == 'text_input'}
            />
          );
        }
        break;
      case 'idle':
      default:
        response_pane = <EvaluatorIdleResponse {...this.props} />;
        break;
    }

    return (
      <div
        id="right-bottom-pane"
        style={{ width: "100%", backgroundColor: "#eee" }}
      >
        {response_pane}
      </div>
    );
  }
}


var IdleResponseHolder = {
  // default: leave blank to use original default when no ids match
  Evaluator: EvaluatorIdleResponse,
  Writer: WriterIdleResponse,
};

var TextResponseHolder = {
  // default: leave blank to use original default when no ids match
  Evaluator: EvaluatorResponse,
  'Onboarding Evaluator': EvaluatorResponse,
  Writer: WriterResponse,
  'Onboarding Writer': WriterResponse,
};

var ResponsePaneHolder = {
  // default: leave blank to use original default when no ids match
  Writer: ResponsePaneWriter,
  Evaluator: ResponsePaneyEvaluator,
};

export default {
  // ComponentName: CustomReplacementComponentMap
  XResponsePane:  ResponsePaneHolder,
};
// XTextResponse: { default: TextResponseHolder},
// XIdleResponse: { default: IdleResponseHolder},
// XResponsePane: { default: ResponsePaneyy }