import React, {Component, useEffect, useState} from "react";
import { ApiService } from "./ApiService";

export default function AddUserTab(){

    const APIService = new ApiService();
    // const [state, setState] = useState(BLANK_STATE);
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("")

    const AddUser = () => {
        APIService.AddUser(username, password).then((outputMessage) => {
            setMessage(outputMessage[0]);
            if("error" in outputMessage){
                setMessage("Error: "+ outputMessage["error"])
            }else if("message" in outputMessage){
                setMessage(outputMessage["message"])
            }
        })
    }

    let handleSubmit = (event) => {
        AddUser()
    }

    let handleUsernameChange = (event) => {
        setUsername(event.target.value)
    }

    let handlePasswordChange = (event) => {
        setPassword(event.target.value)
    }

    return (
        <div>
            <form>
                <label>Username:{"    "}
                    <input type="text" value={username} onChange={(event) => handleUsernameChange(event)} />
                </label>
                <label>   Password:{"    "}
                    <input type="password" value={password} onChange={(event) => handlePasswordChange(event)} />
                </label>
                <input type="button" value="Add a user" onClick={() => handleSubmit()} />
            </form>
            {message}
        </div>
    )
};