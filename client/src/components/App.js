import React, { useState } from "react";
import { Container } from "reactstrap";
import { HomePage } from "./HomePage/HomePage";
import { ApiService } from "./ApiService";

export default function App() {
  const apiService = new ApiService()
  const [state, setState] = useState(BLANK_STATE);

  let healthCheck = () => {
    apiService.healthCheck().then((status) => {
      initialize(status);
    });
  };

  let initialize = (status) => {
    setState(status);
  };

  if (state === BLANK_STATE) {
    healthCheck()
  }

  return (
    <div>
      <Container>
          <HomePage okStatus={state.status}/>
      </Container>
    </div>
  );
}

const BLANK_STATE = {
  status: ""
};
