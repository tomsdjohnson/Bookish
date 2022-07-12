import React, {Component, useEffect, useState} from "react";
import { ApiService } from "./ApiService";

export default function AddBooksTab(){

    const APIService = new ApiService();
    // const [state, setState] = useState(BLANK_STATE);
    const [title, setTitle] = useState("");
    const [author, setAuthor] = useState("");
    const [books, setBooks] = useState([]);
    const [booksRetrieved, setBooksRetrieved] = useState(false);

    let getBooks = () => {
        APIService.getBooks().then((outputBooks) => {
            setBooks(outputBooks.Books);
        })
    }

    const getBooksByTitle = (event) => {
        //alert("hello")
        // APIService.getBooksByTitle(title).then((outputBooks) => {
        //     setBooks(outputBooks.Books);
        // })

    };

    let formatBooks = (books) => {
          return books.map(book => <li>{book.title}</li>)
    }

    let handleTitleChange = (event) => {
        setTitle(event.target.value)
    }

    let handleAuthorChange = (event) => {
        setAuthor(event.target.value)
    }

    return (
        <form onSubmit={(event) => getBooksByTitle(event)}>
            <label>Title:{"    "}
                <input type="text" value={title} onChange={(event) => handleTitleChange(event)} />
            </label>
            <input type="button" value="Add a book" />
        </form>
    )
};

function RefreshButton(props){

    return (
        <button onClick={() => props.toCall()}>
            {props.text}
        </button>
    )
};