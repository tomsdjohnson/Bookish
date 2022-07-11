import React, {Component, useState} from "react";
import { Route } from "react-router";
import { Container } from "reactstrap";
import { HomePage } from "./homePage/HomePage";
import { ApiService } from "./ApiService";

export default function TestButton(){

    const APIService = new ApiService();
    const [state, setState] = useState(BLANK_STATE);

      const initialize = (status) => {
        setState(status);
      };

      let getBooks = () => {
        APIService.getBooks().then((outputStatus) => {
          initialize(outputStatus);
          })
        };

      if (state === BLANK_STATE) {
        getBooks()
      }

    let formatBooks = (books) => {
          return books.map(book => book.title)
    }

    return (
        <button onClick={() => alert(formatBooks(state.Books))}>
            Get Books
        </button>
    )
};

const BLANK_STATE = {
  Books: null
};