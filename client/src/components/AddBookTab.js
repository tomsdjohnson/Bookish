import React, {Component, useEffect, useState} from "react";
import { ApiService } from "./ApiService";

export default function AddBooksTab(){

    const APIService = new ApiService();
    // const [state, setState] = useState(BLANK_STATE);
    const [title, setTitle] = useState("");
    const [author, setAuthor] = useState("");
    const [ISBN, setISBN] = useState("");
    const [copies, setCopies] = useState("");
    const [message, setMessage] = useState("");
    const [books, setBooks] = useState([]);
    const [booksRetrieved, setBooksRetrieved] = useState(false);

    const AddBook = () => {
        APIService.AddBook(title, author, ISBN, copies).then((outputMessage) => {
            setMessage(outputMessage[0]);
            if("error" in outputMessage){
                setMessage("Error: "+ outputMessage["error"])
            }else if("message" in outputMessage){
                setMessage(outputMessage["message"])
            }
        })
    }

    let handleSubmit = (event) => {
        AddBook()
    }

    let handleTitleChange = (event) => {
        setTitle(event.target.value)
    }

    let handleAuthorChange = (event) => {
        setAuthor(event.target.value)
    }

    let handleISBNChange = (event) => {
        setISBN(event.target.value)
    }

    let handleCopiesChange = (event) => {
        setCopies(event.target.value)
    }

    return (
        <div>
            <form>
                <label>Title:{"    "}
                    <input type="text" value={title} onChange={(event) => handleTitleChange(event)} />
                </label>
                <label>   Author:{"    "}
                    <input type="text" value={author} onChange={(event) => handleAuthorChange(event)} />
                </label>
                <label>   ISBN:{"    "}
                    <input type="text" value={ISBN} onChange={(event) => handleISBNChange(event)} />
                </label>
                <label>   Copies:{"    "}
                    <input type="text" value={copies} onChange={(event) => handleCopiesChange(event)} />
                </label>
                <input type="button" value="Add a book" onClick={() => handleSubmit()} />
            </form>
            {message}
        </div>
    )
};