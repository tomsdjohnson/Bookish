import React, {Component, useEffect, useState} from "react";
import { ApiService } from "./ApiService";

export default function BorrowBookTab(){

    const APIService = new ApiService();
    // const [state, setState] = useState(BLANK_STATE);
    const [title, setTitle] = useState("");
    const [author, setAuthor] = useState("");
    const [books, setBooks] = useState([]);
    const [booksEmpty, setBooksEmpty] = useState(true);
    const [username, setUsername] = useState("")
    const [DueDate, setDueDate] = useState(new Date())
    const [message, setMessage] = useState("")

    useEffect( () => {
        getBooksByTitle("")
    }, [])

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

    const getBooksByAuthor = (inputAuthor) => {
        //alert("hello")
        APIService.DynamicSearchBookByAuthor(inputAuthor).then((outputBooks) => {
            if ('error' in outputBooks) {
                setBooks([])
                setBooksEmpty(true)
            }else{
                setBooks(outputBooks["Books"])
                setBooksEmpty(false)
            }
        })
    };

    let callBorrowAPI = (book) => {
        APIService.BorrowBook(username, book.ISBN, DueDate).then((outputMessage) => {
            setMessage(outputMessage[0]);
        })
    }

    let getBorrowButton = (book) => {
        return Button({text: "Borrow", toCall: })
    }

    let formatBooks = (books) => {
          return books.map(book => <tr><td width="550">{book.title}</td> <td width="550">{book.author}</td> <td width="550">{book.ISBN}</td>{getBorrowButton(book)}</tr>)
    }

    let handleTitleChange = (event) => {
        setAuthor("")
        setTitle(event.target.value)
        getBooksByTitle(event.target.value)
    }

    let handleAuthorChange = (event) => {
        setTitle("")
        setAuthor(event.target.value)
        getBooksByAuthor(event.target.value)
    }

    let printBooks = () => {
        if(!booksEmpty){
            return (<table>
                        <tr>
                            <th>Title</th>
                            <th>Author</th>
                            <th>ISBN</th>
                        </tr>
                        {formatBooks(books)}
                    </table>
            )

        }else{
            return (<text>No books found.</text>)
        }
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
            </form>

            {printBooks()}
        </div>

    )
};

function Button(props){

    return (
        <button onClick={() => props.toCall()}>
            {props.text}
        </button>
    )
};