import React, {Component, useEffect, useState} from "react";
import { ApiService } from "./ApiService";

export default function ListOfBooksTab(){

    const APIService = new ApiService();
    // const [state, setState] = useState(BLANK_STATE);
    const [books, setBooks] = useState([]);
    const [booksRetrieved, setBooksRetrieved] = useState(false);

      useEffect(() =>{
        if(!booksRetrieved) {
            APIService.getBooks().then((outputBooks) => {
                setBooks(outputBooks.Books);
                setBooksRetrieved(true);
            })
        }
     })

      let getBooks = () => {
        APIService.getBooks().then((outputBooks) => {
          setBooks(outputBooks.Books);
          })
        };

    let formatBooks = (books) => {
          return books.map(book => <li>{book.title}</li>)
    }

    return (
        <div>
            <RefreshButton toCall = {getBooks} text = "Refresh"/>
            {formatBooks(books)}
        </div>
    )
};

function RefreshButton(props){

    return (
        <button onClick={() => props.toCall()}>
            {props.text}
        </button>
    )
};
