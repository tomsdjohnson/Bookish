export class ApiService {
  healthCheck() {
    return new Promise((resolve) =>
      fetch("/healthcheck", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
            "Accept": "application/json"
        },
      })
        .then((response) => checkResponse(response))
        .then((response) => resolve(response.json()))
        .catch((error) => console.error(error))
    );
  }

  getBooks() {
    return new Promise((resolve) =>
      fetch("/GetBooks", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
            "Accept": "application/json"
        },
      })
        .then((response) => resolve(response.json()))
        .catch((error) => console.error(error))
    );
  }

    DynamicSearchBookByTitle(title) {
        return new Promise((resolve) =>
            fetch("/DynamicSearchBook", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "title": title
                },

            })
                .then((response) => resolve(response.json()))
                .catch((error) => console.error(error))
        );
    }

    DynamicSearchBookByAuthor(author) {
        return new Promise((resolve) =>
            fetch("/DynamicSearchBook", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "author": author
                },

            })
                .then((response) => resolve(response.json()))
                .catch((error) => console.error(error))
        );
    }

    AddBook(title, author, ISBN, copies) {
    return new Promise((resolve) =>
      fetch("/AddBook", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
            "Accept": "application/json"
        },
        body: JSON.stringify({
            "title": title,
            "author": author,
            "ISBN": parseInt(ISBN),
            "copies": parseInt(copies)
        }),
      })
        .then((response) => resolve(response.json()))
        .catch((error) => console.error(error))
    );
  }

  AddUser(username, password) {
    return new Promise((resolve) =>
      fetch("/NewUser", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
            "Accept": "application/json"
        },
        body: JSON.stringify({
            "username": username,
            "password": password
        }),
      })
        .then((response) => resolve(response.json()))
        .catch((error) => console.error(error))
    );
  }
}

const checkResponse = (response) => {
  if (response.ok) {
    return response;
  }
  return response.text().then((e) => {
    throw new Error(e);
  });
};
