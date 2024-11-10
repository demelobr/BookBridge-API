# BookBridge-API
API feita em Flask para facilitar a criação e o gerenciamento de clubes de leitura online.

### Users
Endpoints relacionados aos usuários.

-  `/register` - [POST]
	- **Método:** POST
	- **Descrição:** Registra um novo usuário com as seguintes **informações obrigatórias**: `email` e `password`.
	- **Request body:**
		```
		{
			"email": "exemplo@email.com",
			"password": "suasenha"
		}
		```
	- **Possíveis respostas:**
		```
		{
			"message": "User created successfully!" // 201 Created
		}

		{
			"message": "Email not valid!" // 400 Bad Request
		}
		
		{
			"message": "User already exists!" // 409 Conflict
		}
		
		{
			"message": "An internal error occurred trying to save user!" // 500 Internal Server Error
		}
		```

- `/users/{email}` - [GET]
	- **Método:** GET
	- **Descrição:** Retorna as informações sobre um usuário. É necessário a passagem de um token pois esse endpoint é protegido pelo JWT.
	- **Headers:**
		```
			Authorization: Bearer <JWT_TOKEN>
		```
	- **Possíveis respostas:**
		```
		{
			"id": "iddouser",
			"email": "emaildouser@email.com" // 200 OK
		}
		
		{
			"message": "Access denied!" // 403 Forbidden
		}
		
		{
			"message": "User not exists!" // 404 Not Found
		}
		```

- `/users/{email}` - [PUT]
	- **Método:** PUT
	- **Descrição:** Edita as informações sobre um usuário. É necessário a passagem de um token pois esse endpoint é protegido pelo JWT.
	- **Headers:**
		```
			Authorization: Bearer <JWT_TOKEN>
		```
	- **Request body:**
		```
		{
			"email": "novoemail@email.com",
			"password": "novasenha"
		}
		```
		- **Obs:** Só é necessário passar **apenas os campos que você deseja editar**.
	- **Possíveis respostas:**
		```
		{
			"message": "User edited successfully!" // 200 OK
		}
		
		{
			message": "No data has been changed! // 400 Bad Request
		}
		
		{
			"message": "Access denied!" // 403 Forbidden
		}
		
		{
			"message": "User not exists!" // 404 Not Found
		}
		
		{
			"message": "User already exists!" // 409 Conflict
		}
		
		{
			"message": "An internal error occurred trying to save user!" // 500 Internal Server Error
		}
		```

- `/users/{email}` - [DELETE]
	- **Método:** DELETE
	- **Descrição:** Deleta as informações sobre um usuário. É necessário a passagem de um token pois esse endpoint é protegido pelo JWT, além de ser o próprio usuário deletando suas próprias informações.
	- **Headers:**
		```
			Authorization: Bearer <JWT_TOKEN>
		```
	- **Possíveis respostas:**
		```
		{
			"message": "User deleted successfully!" // 200 OK
		}
		
		{
			"message": "Access denied!" // 403 Forbidden
		}
		
		{
			"message": "User not exists!" // 404 Not Found
		}
		```

- `/login` - [POST]
	- **Método:** POST
	- **Descrição:** Loga com as credenciais de um usuário existente com as seguintes **informações obrigatórias**: `email` e `password`.
	- **Request body:**
		```
		{
			"email": "seuemail@email.com",
			"password": "suasenha"
		}
		```
	- **Possíveis respostas:**
		```
		{
			"access_token": "stringrepresentandootoken" // 200 OK
		}
		
		{
			"message": "Invalid credentials" // 401 Unauthorized
		}
		
		{
			"message": "User not exists!" // 404 Not Found
		}
		```

- `/logout` - [POST]
	- **Método:** POST
	- **Descrição:** Faz logout na conta de um usuário. É necessário a passagem de um token pois esse endpoint é protegido pelo JWT.
	- **Headers:**
		```
			Authorization: Bearer <JWT_TOKEN>
		```
	- **Possíveis respostas:**
		```
		{
			"message": "Successfully logged out!" // 200 OK
		}
		```


### Clubs
Endpoints relacionados aos clubes de livros.

- `/clubs` - [POST]
	- **Método:** POST
	- **Descrição:** Registra um novo clube com as seguintes **informações obrigatórias**: `name`. É necessário a passagem de um token pois esse endpoint é protegido pelo JWT.
	- **Headers:**
		```
			Authorization: Bearer <JWT_TOKEN>
		```
	- **Request body:**
		```
		{
			"name": "nomedoclube"
		}
		```
	- **Possíveis respostas:**
		```
		{
			"message": "Club created successfully!" // 201 Created
		}
		
		{
			"message": "Club already exists!" // 409 Conflict
		}
		
		{
			"message": "An internal error occurred trying to save club!" // 500 Internal Server Error
		}
		```

- `/clubs` - [GET]
	- **Método:** GET
	- **Descrição:** Retorna uma lista com todos os clubes de livros e suas respectivas informações.
	- **Possíveis respostas:**
		```
		[
			{
				"books": [lista de livros do clube],
				"id": 1,
				"name": "nome do clube de livros",
				"owner_id": 1
			},
			{
				"books": [lista de livros do clube],
				"id": 2,
				"name": "nome do clube de livros",
				"owner_id": 2
			}... // 200 OK
		]
		```

- `/clubs/{clubname}` - [GET]
	- **Método:** GET
	- **Descrição:** Retorna um clube de livros a partir do `clubname` passado na url.
	- **Possíveis respostas:**
		```
		{
			"books": [lista de livros do clube],
			"id": 1,
			"name": "nome do clube de livros",
			"owner_id": 1 // 200 Ok
		}
		
		{
			"message": "Club not exists!" // 404 Not Found
		}
		```

- `/clubs/{clubname}` - [PUT]
	- **Método:** PUT
	- **Descrição:** Edita as informações de um clube de livros a partir do `clubname` passado na url. É necessário a passagem de um token pois esse endpoint é protegido pelo JWT.
	- **Headers:**
		```
			Authorization: Bearer <JWT_TOKEN>
		```
	- **Request body:**
		```
		{
			"name": "novonomeparaoclube",
			"owner_id": 2 // novo id para o dono do clube
		}
		```
		- **Obs:** Só é necessário passar **apenas os campos que você deseja editar**.
	- **Possíveis respostas:**
		```
		{
			"message": "Club edited successfully!" // 200 OK
		}
		
		{
			"message": "No data has been changed!" // 400 Bad Request
		}
		
		{
			"message": "Access denied!" // 403 Forbidden
		}
		
		{
			"message" : "Club not exists!" // 404 Not Found
		}
		
		{
			"message": "User not exists!" // 404 Not Found
		}
		
		{
			"message": "Club already exists!" // 409 Conflict
		}
		
		{
			"message": "An internal error occurred trying to save user!" // 500 Internal Server Error
		}
		```

- `/clubs/{clubname}` - [DELETE]
	- **Método:** DELETE
	- **Descrição:** Deleta as informações sobre um clube de livros a partir do `clubname` passado na url. É necessário a passagem de um token pois esse endpoint é protegido pelo JWT.
	- **Headers:**
		```
			Authorization: Bearer <JWT_TOKEN>
		```
	- **Possíveis respostas:**
		```
		{
			"message": "Club deleted successfully!" // 200 OK
		}
		
		{
			"message": "Access denied!" // 403 Forbidden
		}
		
		{
			"message": "Club not exists!" // 404 Not Found
		}
		```

- `/clubs/addbook/{clubname}/{booktitle}` - [POST]
	- **Método:** POST
	- **Descrição:** Registra um novo livro para a lista de um clube de livros com as seguintes **informações obrigatórias**: `clubname`  para o nome do clube e `booktitle` para o nome do livro, ambas informações passadas na url . É necessário a passagem de um token pois esse endpoint é protegido pelo JWT.
	- **Headers:**
		```
			Authorization: Bearer <JWT_TOKEN>
		```
	- **Possíveis respostas:**
		```
		{
			"message": "Book added to club successfully!" // 200 OK
		}
		
		{
			"message": "Access denied!" // 403 Forbidden
		}
		
		{
			"message": "Club not exists!" // 404 Not Found
		}
		
		{
			"message": "Book not exists!" // 404 Not Found
		}
		
		{
			"message": "This book already exists in this club!" // 409 Conflict
		}
		
		{
			"message": "An internal error occurred trying to save user!" // 500 Internal Server Error
		}
		```

- `/clubs/average-books-read` - [GET]
	- **Método:** GET
	- **Descrição:** Retorna a média de livros lidos por cada clube de livros no geral.
	- **Possíveis respostas:**
		```
		{
			"average number of books read by clubs": 1.5 // 200 Ok
		}
		```


### Books
Endpoints relacionados aos livros.

- `/books` - [POST]
	- **Método:** POST
	- **Descrição:** Registra um novo livro com as seguintes **informações obrigatórias**: `title`, `description`, `gender`. É necessário a passagem de um token pois esse endpoint é protegido pelo JWT.
	- **Headers:**
		```
			Authorization: Bearer <JWT_TOKEN>
		```
	- **Request body:**
		```
		{
			"title": "titulodolivro",
			"description": "descricaodolivro",
			"gender": "generodolivro"
		}
		```
	- **Possíveis respostas:**
		```
		{
			"message": "Book created successfully!" // 201 Created
		}
		
		{
			"message": "Book already exists!" // 409 Conflict
		}
		
		{
			"message": "An internal error occurred trying to save club!" // 500 Internal Server Error
		}
		```

- `/books` - [GET]
	- **Método:** GET
	- **Descrição:** Retorna uma lista de todos os livros cadastrados no geral.
	- **Possíveis respostas:**
		```
		[
			{
				"description": "descricaodolivro1",
				"gender": "generodolivro1",
				"id": 1,
				"registered_by": "userqueregistrou",
				"reviews": [lista de reviews do livro1],
				"title": "titulodolivro1"
			},
			{
				"description": "descricaodolivro2",
				"gender": "generodolivro2",
				"id": 2,
				"registered_by": "userqueregistrou",
				"reviews": [lista de reviews do livro2],
				"title": "titulodolivro2"
			}... // 200 OK
		]
		```

- `/books/{booktitle}` - [GET]
	- **Método:** GET
	- **Descrição:** Retorna as informações do livro de nome `booktitle` passado na url.
	- **Possíveis respostas:**
		```
		{
			"description": "descricaodolivro1",
			"gender": "generodolivro1",
			"id": 1,
			"registered_by": "userqueregistrou",
			"reviews": [lista de reviews do livro1],
			"title": "titulodolivro1"
		}
		```

- `/books/{booktitle}` - [PUT]
	- **Método:** PUT
	- **Descrição:** Edita as informações de um livro a partir do `booktitle` passado na url. É necessário a passagem de um token pois esse endpoint é protegido pelo JWT.
	- **Headers:**
		```
			Authorization: Bearer <JWT_TOKEN>
		```
	- **Request body:**
		```
		{
			"title": "novotitulo",
			"description": "novadescricaodolivro",
			"gender": "novogenerodolivro"
		}
		```
		- **Obs:** Só é necessário passar **apenas os campos que você deseja editar**.
	- **Possíveis respostas:**
		```
		{
			"message": "Book edited successfully!" // 200 OK
		}
		
		{
			"message": "No data has been changed!" // 400 Bad Request
		}
		
		{
			"message": "Access denied!" // 403 Forbidden
		}
		
		{
			"message" : "Book not exists!" // 404 Not Found
		}
		
		{
			"message": "User not exists!" // 404 Not Found
		}
		
		{
			"message": "Book already exists!" // 409 Conflict
		}
		
		{
			"message": "An internal error occurred trying to save user!" // 500 Internal Server Error
		}
		```

- `/books/{booktitle}` - [DELETE]
	- **Método:** DELETE
	- **Descrição:** Deleta as informações sobre um livro a partir do `booktitle` passado na url. É necessário a passagem de um token pois esse endpoint é protegido pelo JWT.
	- **Headers:**
		```
			Authorization: Bearer <JWT_TOKEN>
		```
	- **Possíveis respostas:**
		```
		{
			"message": "Book deleted successfully!" // 200 OK
		}
		
		{
			"message": "Access denied!" // 403 Forbidden
		}
		
		{
			"message": "Book not exists!" // 404 Not Found
		}
		```


### Reviews
Endpoints relacionados às reviews.

- `/reviews` - [POST]
	- **Método:** POST
	- **Descrição:** Registrar uma nova review com as seguintes **informações obrigatórias**: `rating`, `comment`, `book_title`. É necessário a passagem de um token pois esse endpoint é protegido pelo JWT.
	- **Headers:**
		```
			Authorization: Bearer <JWT_TOKEN>
		```
	- **Request body:**
		```
		{
			"rating": "5",
			"comment": "livro muito legal",
			"book_title": "titulodolivro"
		}
		```
		- **Possíveis respostas:**
		```
		{
			"message": "Review created successfully!" // 201 Created
		}
		
		{
			"message": "The review value must be from 0 to 5!" // Bad Request
		}
		
		{
			"message": "Information is missing to make a review!" // Bad Request
		}
		
		{
			"message": "Book not exists!" // 404 Not Found
		}
		
		{
			"message": "An internal error occurred trying to save club!" // 500 Internal Server Error
		}
		```

- `/reviews` - [GET]
	- **Método:** GET
	- **Descrição:** Retorna uma lista de todas as reviews cadastradas no geral.
	- **Possíveis respostas:**
		```
		[
			{
				"book_title": "nomedolivro1",
				"comment": "comentariosobreolivro1",
				"created_at": "dataehora",
				"id": 1,
				"rating": 5,
				"user_email": "emaildoautor@email.com"
			},
			{
				"book_title": "nomedolivro2",
				"comment": "comentariosobreolivro2",
				"created_at": "dataehora",
				"id": 2,
				"rating": 4,
				"user_email": "emaildoautor@email.com"
			}... // 200 OK
		]
		```

- `/reviews/{booktitle}` - [GET]
	- **Método:** GET
	- **Descrição:** Retorna uma lista de todas as reviews sobre um livro de nome `booktitle` passado na url.
	- **Possíveis respostas:**
		```
		[
			{
				"book_title": "nomedolivro1",
				"comment": "comentariosobreolivro1",
				"created_at": "dataehora",
				"id": 1,
				"rating": 5,
				"user_email": "emaildoautor@email.com"
			},
			{
				"book_title": "nomedolivro1",
				"comment": "comentariosobreolivro1",
				"created_at": "dataehora",
				"id": 2,
				"rating": 4,
				"user_email": "emaildoautor@email.com"
			}... // 200 OK
		]
		```

- `/reviews/{id}` - [GET]
	- **Método:** GET
	- **Descrição:** Retorna uma reviews sobre um livro de identificação `id` passada na url.
	- **Possíveis respostas:**
		```
		{
			"book_title": "nomedolivro1",
			"comment": "comentariosobreolivro1",
			"created_at": "dataehora",
			"id": 1,
			"rating": 5,
			"user_email": "emaildoautor@email.com"
		}
		```

- `/reviews/{id}` - [PUT]
	- **Método:** PUT
	- **Descrição:** Edita as informações de uma review a partir da identificação `id` passada na url. É necessário a passagem de um token pois esse endpoint é protegido pelo JWT.
	- **Headers:**
		```
			Authorization: Bearer <JWT_TOKEN>
		```
	- **Request body:**
		```
		{
			"rating": "5",
			"comment": "novocomentariosobreolivro",
			"user_email": "novoemail@email.com",
			"book_title": "novotitulo"
		}
		```
		- **Obs:** Só é necessário passar **apenas os campos que você deseja editar**.
	- **Possíveis respostas:**
		```
		{
			"message": "Review edited successfully!" // 200 OK
		}
		
		{
			"message": "No data has been changed!" // 400 Bad Request
		}
		
		{
			"message": "The review value must be from 0 to 5!" // 400 Bad Request
		}
		
		{
			"message": "Access denied!" // 403 Forbidden
		}
		
		{
			"message" : "Book not exists!" // 404 Not Found
		}
		
		{
			"message": "Review not exists!" // 404 Not Found
		}
		
		{
			"message": "An internal error occurred trying to save user!" // 500 Internal Server Error
		}
		```

- `/reviews/{id}` - [DELETE]
	- **Método:** DELETE
	- **Descrição:** Deleta as informações sobre uma review a partir da identificação `id` passada na url. É necessário a passagem de um token pois esse endpoint é protegido pelo JWT.
	- **Headers:**
		```
			Authorization: Bearer <JWT_TOKEN>
		```
	- **Possíveis respostas:**
		```
		{
			"message": "Review deleted successfully!" // 200 OK
		}
		
		{
			"message": "Access denied!" // 403 Forbidden
		}
		
		{
			"message": "Review not exists!" // 404 Not Found
		}
		```

- `/reviews/avarage-rating/{booktitle}` - [GET]
	- **Método:** GET
	- **Descrição:** Retorna a nota média de um livro de título `booktitle` passada na url.
	- **Possíveis respostas:**
		```
		{
			"avarage rating of book": 4.5 // 200 Ok
		}
		```