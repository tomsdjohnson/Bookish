import React, {Component, useEffect, useState} from "react";
import { ApiService } from "./ApiService";

export default function SearchBooksTab(){

    const APIService = new ApiService();
    // const [state, setState] = useState(BLANK_STATE);
    const [title, setTitle] = useState("");
    const [author, setAuthor] = useState("");
    const [books, setBooks] = useState([]);
    const [booksEmpty, setBooksEmpty] = useState(true);
    const [booksRetrieved, setBooksRetrieved] = useState(false);

    const getBooksByTitle = (inputTitle) => {
        //alert("hello")
        APIService.DynamicSearchBookByTitle(inputTitle).then((outputBooks) => {
            if ('error' in outputBooks) {
                setBooks([])
                setBooksEmpty(true)
            }else{
                setBooks(outputBooks["Books"])
                setBooksEmpty(false)
            }
        })
    };

    let formatBooks = (books) => {
          return books.map(book => <li>{book.title}</li>)
    }

    let handleTitleChange = (event) => {
        setTitle(event.target.value)
        getBooksByTitle(event.target.value)
    }

    let handleAuthorChange = (event) => {
        setAuthor(event.target.value)
    }

    let printBooks = () => {
        if(!booksEmpty){
            return formatBooks(books)
        }else{
            return (<text>No books found.</text>)
        }
    }

    return (
        <div>
            <form onSubmit={(event) => getBooksByTitle(event)}>
                <label>Title:{"    "}
                    <input type="text" value={title} onChange={(event) => handleTitleChange(event)} />
                </label>
                <input type="button" value="Search by title" />
            </form>
            {printBooks()}
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