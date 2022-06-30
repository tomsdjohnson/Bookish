import React, { Component } from "react";
import {
  HomeDiv,
  HomeTitleTag,
  HomeTitleContainer,
} from "./HomeComponents";

export class HomePage extends Component {
  constructor(props) {
    super(props);

    this.state = {example: props.example};
  }

  render() {
    return (
      <HomeDiv>
        <HomeTitleContainer>
          <HomeTitleTag>Example</HomeTitleTag>
          <li>{this.state.example.data1}</li>
          <li>{this.state.example.data2}</li>
        </HomeTitleContainer>
      </HomeDiv>
    );
  }
}
