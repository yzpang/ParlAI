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
  Col,
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

class Hourglass extends React.Component {
  render() {
    // TODO move to CSS document
    let hourglass_style = {
      marginTop: '-1px',
      marginRight: '5px',
      display: 'inline',
      float: 'left',
    };

    // TODO animate?
    return (
      <div id="hourglass" style={hourglass_style}>
        <span className="glyphicon glyphicon-hourglass" aria-hidden="true" />
      </div>
    );
  }
}

class EvaluatorWaitingMessage extends React.Component {
  render() {
    let message_style = {
      float: 'left',
      display: 'table',
      backgroundColor: '#fff',
    };
    let text = 'Waiting for the writers to compose their claims...';
    if (this.props.world_state == 'waiting') {
      text = 'Waiting to pair with a task...';
    }
    return (
      <div
        id="waiting-for-message"
        className="row"
        style={{ marginLeft: '0', marginRight: '0' }}
      >
        <div className="alert alert-warning" role="alert" style={message_style}>
          <Hourglass />
          <span style={{ fontSize: '16px' }}>{text}</span>
        </div>
      </div>
    );
  }
}

class WriterWaitingMessage extends React.Component {
  render() {
    let message_style = {
      float: 'left',
      display: 'table',
      backgroundColor: '#fff',
    };
    let text = 'Waiting for the rankers to rank your claims...';
    if (this.props.world_state == 'waiting') {
      text = 'Waiting to pair with a task...';
    }
    return (
      <div
        id="waiting-for-message"
        className="row"
        style={{ marginLeft: '0', marginRight: '0' }}
      >
        <div className="alert alert-warning" role="alert" style={message_style}>
          <Hourglass />
          <span style={{ fontSize: '16px' }}>{text}</span>
        </div>
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
      height: '300px',
      overflowY: 'scroll',
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
        Please write a claim that is <font color="#E8684C"> Definitely Correct </font> about the situation or event in the prompt,
      </div>
      );
    let entail_input = (
      <div>
        <ControlLabel>{text_entail}</ControlLabel>
        <FormControl
          componentClass="textarea"
          rows="3"
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
        Please write a claim that is <font color="#E8684C"> Definitely Incorrect </font> about the situation or event in the prompt,
      </div>
      );
    let contradict_input = (
      <div>
        <ControlLabel>{text_contradict}</ControlLabel>
        <FormControl
          componentClass="textarea"
          rows="3"
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
        Please write a claim that is <font color="#E8684C"> Neither </font> definitely correct nor definitely incorrect about the situation or event in the prompt,
      </div>
      );
    let neutral_input = (
      <div>
        <ControlLabel>{text_neutral}</ControlLabel>
        <FormControl
          componentClass="textarea"
          rows="3"
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
        Submit
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
    this.state = { 
      textreason: '',
      claimChoice: '',
      validation1: '',
      validation2: '',
      sending: false};
    this.handleInputChange = this.handleInputChange.bind(this);
  }

  componentDidUpdate(prevProps, prevState, snapshot) {
    // Only change in the active status of this component should cause a
    // focus event. Not having this would make the focus occur on every
    // state update (including things like volume changes)
    if (this.props.active && !prevProps.active) {
      $('input#id_text_input').focus();
    }
    this.props.onInputResize();
  }

  // tryMessageSend() {
  //   if ((this.state.accept1 != '' || this.state.reject1 != '') && (this.state.accept2 != '' || this.state.reject2 != '') && this.state.claimChoice != '' && this.props.active && !this.state.sending) {
  //     this.setState({ sending: true });
  //     this.props.onMessageSend(this.state.accept1, this.state.reject1, this.state.accpet2, this.state.reject2, this.state.claimChoice, this.state.textreason, {}, () =>
  //       this.setState({ accept1: '', reject1: '', accept2: '', reject2: '', claimChoice: '', textreason: '', sending: false })
  //     );
  //   }
  // }

  tryMessageSend() {
    if (this.props.active && !this.state.sending) {
      this.setState({ sending: true });
      this.props.onMessageSend(this.state.claimChoice, this.state.textreason, this.state.validation1, this.state.validation2, {}, () =>
        this.setState({ claimChoice: '', textreason: '', validation1: '', validation2: '', sending: false })
      );
    }
  }

  handleEnterKey(event) {
    event.preventDefault();
    if (this.props.task_done) {
      this.props.allDoneCallback();
    } else if (this.props.subtask_done && this.props.show_next_task_button) {
      this.props.nextButtonCallback();
    }
  }

  handleKeyPress(e) {
    if (e.key === 'Enter') {
      this.tryMessageSend();
      e.stopPropagation();
      e.nativeEvent.stopImmediatePropagation();
    }
  }

  handleInputChange(event) {
    console.log(event)
    let target = event.target;
    let value = target.value;
    let name = target.name;

    this.setState({ [name]: value });
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
      height: '300px',
      overflowY: 'scroll',
    };
    //  TODO: make height variable, a percentage?
    let input_style = {
      height: '50px',
      width: '100%',
      display: 'block',
      float: 'left',

    };
    let input_inline_style = {
      height: '50px',
      width: '100%',
      display: 'inline-block',
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

    const approvebox  = {
      backgroundColor: '#66B46E',
      borderRadius: 3,
      padding: '5px',
      border: '1px solid #44864B',
      color: 'white',
    }

    const rejectbox  = {
      backgroundColor: '#E8684C',
      borderRadius: 3,
      padding: '5px',
      border: '1px solid #D34000',
      color: 'white',
    }

    const claimbox  = {
      backgroundColor: '#636363',
      borderRadius: 3,
      padding: '5px',
      border: '1px solid #393939',
      color: 'white',
    }

    const inline_text = {
      display: "inline-block",
    };

    const approve = "Valid"
    const invalid = "Invalid"
    const text_claim1 = "Claim 1"
    const text_claim2 = "Claim 2"
    let validation_buttons_1 = (
      <div>
        <Form
          horizontal
          style={{ backgroundColor: "#eeeeee", paddingBottom: "10px", 
            display: "inline-block" }}
        >
          <div className="container" style={{ width: "auto" }}>
          <ControlLabel> {text_claim1}, </ControlLabel>
            <FormGroup>
              <Col sm={6}>
                <Radio
                  name="validation1"
                  value={approve}
                  style={{ width: "100%" }}
                  checked={this.state.validation1 == approve}
                  onChange={this.handleInputChange}
                >
                  <div style={approvebox}> Approve </div>
                </Radio>
              </Col>
              <Col sm={6}>
                <Radio
                  name="validation1"
                  value={invalid}
                  style={{ width: "100%" }}
                  checked={this.state.validation1 == invalid}
                  onChange={this.handleInputChange}
                >
                  <div style={rejectbox}> Invalid </div>
                </Radio>
              </Col>
            </FormGroup>
          </div>
        </Form>
      </div>
    );

    let validation_buttons_2 = (
      <div>
        <Form
          horizontal
          style={{ backgroundColor: "#eeeeee", paddingBottom: "10px",
            display: "inline-block" }}
        >
          <div className="container" style={{ width: "auto" }}>
          <ControlLabel> {text_claim2}, </ControlLabel>
            <FormGroup>
              <Col sm={6}>
                <Radio
                  name="validation2"
                  value={approve}
                  style={{ width: "100%" }}
                  checked={this.state.validation2 == approve}
                  onChange={this.handleInputChange}
                  onClick={this._showMessage.bind(null, true)}
                >
                  <div style={approvebox}> Approve </div>
                </Radio>
              </Col>
              <Col sm={6}>
                <Radio
                  name="validation2"
                  value={invalid}
                  style={{ width: "100%" }}
                  checked={this.state.validation2 == invalid}
                  onChange={this.handleInputChange}
                  onClick={this._showMessage.bind(null, true)}
                >
                  <div style={rejectbox}> Invalid </div>
                </Radio>
              </Col>
            </FormGroup>
          </div>
        </Form>
      </div>
    );

    // const s1_name = "Claim 1";
    // const s2_name = "Claim 2"
    const text_rank1 = "Which claim do you think is better?" ;
    // onSubmit={this.handleEnterKey}

    let rank1 = (
      <div>
        <Form
          horizontal
          style={{ backgroundColor: "#eeeeee", paddingBottom: "10px",
            display: "inline-block" }}
        >
          <div className="container" style={{ width: "auto" }}>
            <ControlLabel> {text_rank1} </ControlLabel>
            <FormGroup>
              <Col sm={6}>
                <Radio
                  name="claimChoice"
                  value={text_claim1}
                  style={{ width: "100%" }}
                  checked={this.state.claimChoice == text_claim1}
                  onChange={this.handleInputChange}
                >
                  <div style={claimbox}> Claim 1 </div>
                </Radio>
              </Col>
              <Col sm={6}>
                <Radio
                  name="claimChoice"
                  value={text_claim2}
                  style={{ width: "100%" }}
                  checked={this.state.claimChoice == text_claim2}
                  onChange={this.handleInputChange}
                >
                  <div style={claimbox}> Claim 2 </div>
                </Radio>
              </Col>
            </FormGroup>
            {text_reason}
          </div>
        </Form>
      </div>
    );

    let text_reasoning = (
      <div>
        Optionally (but encouraged), please provide a brief justification for your ranking
      </div>
      );
    let text_reason = (
      <div>
        <ControlLabel>{text_reasoning}</ControlLabel>
        <FormControl
          type="text"
          id="id_textreason"
          name="textreason"
          style={{
            width: '80%',
            height: '100%',
            float: 'left',
            fontSize: '16px',
          }}
          value={this.state.textreason}
          placeholder="Optionally add your justification here..."
          onKeyPress={e => this.handleKeyPress(e)}
          onChange={this.handleInputChange}
          disabled={!this.props.active || this.state.sending}
        />
      </div>
    );

    let submit_button = (
      <Button
        className="btn btn-primary"
        style={submit_style}
        id="id_send_msg_button"
        disabled={!this.props.active || this.state.sending
        }
        onClick={() => this.tryMessageSend()}
      >
        Submit
      </Button>
    );

    return (
      <div
        id="response-type-text-input"
        className="response-type-module"
        style={pane_style}
      >
        <div style={input_style}>
          {validation_buttons_1}
          {validation_buttons_2}
          { this.state.showMessage && (
              <div>
                {rank1}
                {text_reason}
              </div> )}
          {submit_button}
        </div>
      </div>
    );
  }
}
// { this.state.showMessage && (<div style={input_style}>{rank1}</div>) }
// <div
//   id="response-type-text-input"
//   className="response-type-module"
//   style={pane_style}
// >
//   <div style={{ width: "auto" }}>
//     <div>Claims 1: {approve_button1} {reject_button1} <br /></div>
//     <div>Claims 2: {approve_button2} {reject_button2} <br /></div>
//   </div>
//   <div style={input_style}>{rank1}</div>
//   <div style={input_style}>
//   <br /><br />
//   {text_reason}{submit_button}
//   </div>
// </div>

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
  Writer0: ResponsePaneWriter,
  Writer1: ResponsePaneWriter,
  Evaluator0: ResponsePaneyEvaluator,
  Evaluator1: ResponsePaneyEvaluator,
};

var WaitingResponseHolder = {
  Writer0: WriterWaitingMessage,
  Writer1: WriterWaitingMessage,
  Evaluator0: EvaluatorWaitingMessage,
  Evaluator1: EvaluatorWaitingMessage,
}

export default {
  // ComponentName: CustomReplacementComponentMap
  // XTextResponse:  TextResponseHolder,
  // XIdleResponse:  IdleResponseHolder,
  XWaitingMessage: WaitingResponseHolder,
  XResponsePane:  ResponsePaneHolder,
};
