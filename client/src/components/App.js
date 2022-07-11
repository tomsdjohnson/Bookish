import React, {Component, useState} from "react";
import { Route } from "react-router";
import { Container } from "reactstrap";
import { HomePage } from "./homePage/HomePage";
import { ApiService } from "./ApiService";

export default function App() {

  const APIService = new ApiService()
  const [state, setState] = useState(BLANK_STATE);

  const initialize = (status) => {
    setState(status);
  };

  let healthCheck = () => {
    APIService.healthCheck().then((outputStatus) => {
      initialize(outputStatus);
      })
    };

  if (state === BLANK_STATE) {
    healthCheck()
  }

  return (
    <div>
      <Container>
          <HomePage okStatus={state.status} />
      </Container>
    </div>
    );

}

const BLANK_STATE = {
  example: {
    id: null,
    data1: null,
    data2: null
  },
  status: "",
};
