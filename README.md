# Actividad 4 - Gestión de Empresas y Usuarios con FastAPI, PostgreSQL y GraphQL

## 1. Descripción

Esta actividad consiste en desarrollar un backend para la gestión de empresas y usuarios asociados a cada empresa.

El proyecto implementa una API mediante FastAPI y GraphQL, utilizando PostgreSQL como sistema gestor de base de datos. La aplicación utiliza SQLAlchemy para el acceso a datos y Alembic para controlar las migraciones de la base de datos.

Además, el proyecto se ejecuta mediante Docker Compose, utilizando contenedores independientes para FastAPI, PostgreSQL y pgAdmin.

Como parte de la actividad se implementó la relación `Empresa–Usuario` mediante la entidad intermedia `CompanyUser`, además de autenticación mediante correo y contraseña, generación de tokens JWT y administración de usuarios por empresa.

## 2. Tecnologías utilizadas

- Python 3.11
- FastAPI
- Uvicorn
- PostgreSQL
- SQLAlchemy
- Psycopg
- Alembic
- Strawberry GraphQL
- pwdlib con Argon2
- PyJWT
- email-validator
- Docker
- Docker Compose
- pgAdmin 4

## 3. Arquitectura del proyecto

El backend utiliza una arquitectura por capas para separar las responsabilidades de cada componente.

```text
Cliente GraphQL
      |
      v
   FastAPI
      |
      v
   GraphQL
      |
      v
Queries / Mutations
      |
      v
   Services
      |
      v
 Repositories
      |
      v
  SQLAlchemy
      |
      v
 PostgreSQL
```

### Responsabilidades principales

| Componente | Responsabilidad |
|---|---|
| `graphql_api` | Define el esquema GraphQL, queries, mutations y tipos |
| `services` | Contiene la lógica de negocio |
| `repositories` | Gestiona el acceso y las operaciones sobre los datos |
| `models` | Define las tablas mediante modelos SQLAlchemy |
| `database` | Configura la conexión con PostgreSQL |
| `security` | Gestiona contraseñas, autenticación y JWT |
| `alembic` | Gestiona las migraciones de la base de datos |

## 4. Estructura del proyecto

```text
actividad4_david_morales/
│
├── alembic/
│   ├── versions/
│   │   ├── d2b4557bb05a_crear_tabla_users.py
│   │   ├── 2fc7a8162604_crear_relacion_empresa_usuario.py
│   │   └── b5eaa79d5e9f_garantizar_un_administrador_principal_.py
│   ├── env.py
│   ├── README
│   └── script.py.mako
│
├── database/
│   ├── database.py
│   └── __init__.py
│
├── graphql_api/
│   ├── __init__.py
│   ├── mutations.py
│   ├── queries.py
│   ├── schema.py
│   └── types.py
│
├── models/
│   ├── company.py
│   ├── company_user.py
│   ├── user.py
│   └── __init__.py
│
├── repositories/
│   ├── company_repository.py
│   ├── company_user_repository.py
│   ├── user_repository.py
│   └── __init__.py
│
├── security/
│   ├── auth.py
│   └── jwt.py
│
├── services/
│   ├── auth_service.py
│   ├── company_service.py
│   ├── company_user_service.py
│   └── user_service.py
│
├── .dockerignore
├── .env.example
├── .gitignore
├── alembic.ini
├── compose.yaml
├── Dockerfile
├── main.py
├── README.md
└── requirements.txt
```

## 5. Modelo de datos

La actividad utiliza tres entidades principales para representar la relación entre empresas y usuarios.

```text
COMPANY
   |
   | 1:N
   |
   v
COMPANY_USER
   ^
   |
   | N:1
   |
  USER
```

### Company

La entidad `Company` representa a las empresas registradas en el sistema.

Entre sus principales atributos se encuentran:

- `id`
- `name`
- `legal_name`
- `tax_id`
- `email`
- `phone`
- `is_active`
- `created_at`
- `updated_at`

### User

La entidad `User` representa a los usuarios del sistema.

Entre sus principales atributos se encuentran:

- `id`
- `name`
- `email`
- `password_hash`
- `email_verified`
- `is_active`
- `created_at`
- `updated_at`

### CompanyUser

La entidad `CompanyUser` representa la relación entre una empresa y un usuario.

Contiene:

- `id`
- `company_id`
- `user_id`
- `is_admin`
- `is_active`
- `joined_at`

La relación permite almacenar información específica del usuario dentro de una empresa.

## 6. Relación Empresa–Usuario

La relación entre `Company` y `User` se implementa mediante `CompanyUser`.

Esto permite mantener separada la información global del usuario de la información correspondiente a su relación con una empresa.

Por ejemplo, un usuario puede tener:

```text
User
├── id
├── name
├── email
└── password_hash
```

Y su relación con una empresa puede contener:

```text
CompanyUser
├── company_id
├── user_id
├── is_admin
├── is_active
└── joined_at
```

También se establecieron relaciones ORM mediante SQLAlchemy:

```python
company_users = relationship(
    "CompanyUser",
    back_populates="company"
)
```

y:

```python
company = relationship(
    "Company",
    back_populates="company_users"
)

user = relationship(
    "User",
    back_populates="company_users"
)
```

## 7. Regla del administrador principal

Una de las reglas principales de la actividad establece que una empresa solamente puede tener un administrador principal.

La regla se implementó en la lógica de negocio y también directamente en PostgreSQL mediante un índice único parcial.

```sql
CREATE UNIQUE INDEX uq_company_principal_admin
ON company_users (company_id)
WHERE is_admin = true;
```

Con esta restricción, PostgreSQL impide que una misma empresa tenga dos registros con:

```text
is_admin = true
```

Cuando se intenta registrar un segundo administrador para la misma empresa, la aplicación devuelve:

```text
La empresa ya tiene un administrador principal
```

## 8. Autenticación y seguridad

El proyecto implementa autenticación mediante correo electrónico y contraseña.

Las contraseñas no se almacenan directamente en la base de datos.

El flujo utilizado es:

```text
Contraseña
    |
    v
Validación
    |
    v
Argon2
    |
    v
password_hash
    |
    v
PostgreSQL
```

Para realizar la autenticación se utiliza la mutation `login`.

El flujo de autenticación es:

```text
Correo + contraseña
        |
        v
Buscar usuario
        |
        v
Verificar contraseña
        |
        v
Comprobar usuario activo
        |
        v
Generar JWT
        |
        v
Token Bearer
```

El token generado utiliza JWT y contiene información necesaria para identificar al usuario autenticado.

Las operaciones protegidas utilizan el siguiente encabezado:

```text
Authorization: Bearer <token>
```

## 9. Hash de contraseñas

Para proteger las contraseñas se utiliza Argon2 mediante `pwdlib`.

El valor almacenado en la base de datos corresponde al hash de la contraseña y no a la contraseña original.

Ejemplo del formato almacenado:

```text
$argon2id$...
```

Esto permite verificar posteriormente la contraseña mediante el hash almacenado sin guardar la contraseña original.

## 10. Validación de correos

Los correos electrónicos son normalizados y validados antes de crear un usuario.

La aplicación utiliza `email-validator`.

Un correo con formato incorrecto es rechazado.

Ejemplo:

```text
correo-invalido
```

Respuesta:

```text
El correo electrónico no es válido
```

También se valida que el correo no se encuentre registrado previamente.

Si el correo ya existe:

```text
El correo electrónico ya está registrado
```

## 11. Esquema GraphQL

El proyecto utiliza Strawberry GraphQL para definir la API.

Los identificadores utilizan `ID` y los campos de fecha utilizan el escalar personalizado `Time`.

### Tipo User

```graphql
type User {
  id: ID!
  name: String!
  email: String!
  emailVerified: Boolean!
  isActive: Boolean!
  createdAt: Time!
  updatedAt: Time!
}
```

### Tipo CompanyUser

```graphql
type CompanyUser {
  id: ID!
  companyId: ID!
  userId: ID!
  isAdmin: Boolean!
  isActive: Boolean!
  joinedAt: Time!
  company: Company!
  user: User!
}
```

### LoginInput

```graphql
input LoginInput {
  email: String!
  password: String!
}
```

### AuthUser

```graphql
type AuthUser {
  id: ID!
  name: String!
  email: String!
}
```

### AuthPayload

```graphql
type AuthPayload {
  token: String!
  tokenType: String!
  user: AuthUser!
}
```

### CreateCompanyAdminInput

```graphql
input CreateCompanyAdminInput {
  companyId: ID!
  name: String!
  email: String!
  password: String!
}
```

### CreateCompanyUserInput

```graphql
input CreateCompanyUserInput {
  companyId: ID!
  name: String!
  email: String!
  password: String!
}
```

## 12. Queries

La consulta principal relacionada con la actividad es:

```graphql
companyUsers(companyId: ID!): [CompanyUser!]!
```

Esta query permite obtener todos los usuarios relacionados con una empresa.

Ejemplo:

```graphql
query {
  companyUsers(companyId: "1") {
    id
    companyId
    userId
    isAdmin
    isActive
    joinedAt
    company {
      id
      name
      legalName
      isActive
    }
    user {
      id
      name
      email
      emailVerified
      isActive
    }
  }
}
```

Esta consulta también permite comprobar las relaciones anidadas entre:

```text
CompanyUser
    |
    +-- Company
    |
    +-- User
```

## 13. Mutations

Las principales mutations implementadas son:

| Mutation | Descripción |
|---|---|
| `createCompany` | Crea una empresa |
| `updateCompany` | Actualiza una empresa |
| `deactivateCompany` | Desactiva una empresa |
| `login` | Autentica un usuario y genera un JWT |
| `createCompanyAdmin` | Crea el administrador principal |
| `createCompanyUser` | Crea un usuario dentro de una empresa |
| `deactivateCompanyUser` | Desactiva la relación del usuario con una empresa |

### Crear administrador principal

```graphql
mutation {
  createCompanyAdmin(
    input: {
      companyId: "1"
      name: "David Morales"
      email: "admin@demo.com"
      password: "Datos2026"
    }
  ) {
    id
    companyId
    userId
    isAdmin
    isActive
  }
}
```

### Crear usuario de empresa

Esta operación requiere autenticación mediante un JWT de un administrador de la empresa.

```graphql
mutation {
  createCompanyUser(
    input: {
      companyId: "1"
      name: "Usuario Demo"
      email: "usuario@demo.com"
      password: "Usuario2026"
    }
  ) {
    id
    companyId
    userId
    isAdmin
    isActive
  }
}
```

### Desactivar usuario de empresa

```graphql
mutation {
  deactivateCompanyUser(id: "2") {
    id
    companyId
    userId
    isAdmin
    isActive
  }
}
```

La desactivación se realiza sobre `CompanyUser`.

Por lo tanto, el usuario puede continuar existiendo como usuario global mientras su relación específica con una empresa se encuentra inactiva.

## 14. Migraciones con Alembic

El proyecto utiliza Alembic para controlar la estructura y evolución de la base de datos.

Durante la actividad se agregaron las siguientes migraciones principales:

```text
d2b4557bb05a_crear_tabla_users.py
2fc7a8162604_crear_relacion_empresa_usuario.py
b5eaa79d5e9f_garantizar_un_administrador_principal_.py
```

### Crear tabla de usuarios

La primera migración relacionada con usuarios crea la tabla `users`.

Esta tabla contiene información como:

```text
id
name
email
password_hash
email_verified
is_active
created_at
updated_at
```

### Crear relación Empresa–Usuario

La segunda migración crea la tabla `company_users`.

Esta tabla contiene las claves foráneas:

```text
company_id -> companies.id
user_id    -> users.id
```

Además, contiene los campos:

```text
is_admin
is_active
joined_at
```

### Garantizar un administrador principal

La tercera migración agrega la restricción que garantiza que una empresa no tenga más de un administrador principal.

La restricción se implementa mediante un índice único parcial sobre:

```text
company_id
```

cuando:

```text
is_admin = true
```

## 15. Docker

El proyecto se ejecuta mediante Docker Compose.

Los servicios principales son:

```text
FastAPI
PostgreSQL
pgAdmin
```

### Puertos utilizados

| Servicio | Puerto |
|---|---:|
| FastAPI | 8001 |
| PostgreSQL | 5433 |
| pgAdmin | 5051 |

La comunicación entre los contenedores utiliza la red interna de Docker Compose.

Dentro del contenedor de FastAPI, PostgreSQL se encuentra disponible mediante:

```text
DB_HOST=postgres
DB_PORT=5432
```

Mientras que el puerto `5433` se utiliza para acceder a PostgreSQL desde el equipo local.

## 16. Variables de entorno

La configuración utiliza variables de entorno mediante un archivo `.env`.

Ejemplo de configuración:

```env
APP_PORT=8001

DB_USER=actividad4_user
DB_PASSWORD=actividad4_pass
DB_HOST=postgres
DB_PORT=5432
DB_NAME=actividad4

POSTGRES_PORT=5433
POSTGRES_USER=actividad4_user
POSTGRES_PASSWORD=actividad4_pass
POSTGRES_DB=actividad4

PGADMIN_PORT=5051
PGADMIN_EMAIL=admin@actividad4.com
PGADMIN_PASSWORD=Datos2026

JWT_SECRET_KEY=actividad4_david_morales_secret_key_2026
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60
```

El archivo `.env` se mantiene fuera del control de versiones mediante `.gitignore`.

Para compartir la configuración del proyecto se utiliza `.env.example`.

## 17. Endpoint GraphQL

La API GraphQL está disponible en:

```text
http://localhost:8001/graphql
```

Al acceder a esta dirección se puede utilizar la interfaz de GraphQL para ejecutar queries y mutations.

La documentación y exploración del esquema permiten consultar los tipos, campos, queries y mutations disponibles.

## 18. Pruebas realizadas

Durante la implementación se realizaron diferentes pruebas funcionales directamente sobre GraphQL.

### Crear empresa

Se verificó el funcionamiento de:

```graphql
createCompany
```

La empresa fue creada correctamente.

### Actualizar empresa

Se verificó:

```graphql
updateCompany
```

La información de la empresa fue actualizada correctamente.

### Desactivar empresa

Se verificó:

```graphql
deactivateCompany
```

La empresa cambió correctamente su estado.

Posteriormente se reactivó para continuar con las pruebas de usuarios.

### Crear administrador principal

Se creó correctamente un administrador para la empresa:

```text
Empresa: Empresa Demo Actualizada
Usuario: David Morales
Correo: admin@demo.com
```

El registro generado presentó:

```text
isAdmin = true
isActive = true
```

### Verificación del hash

Se verificó directamente en la base de datos que la contraseña no se almacena en texto plano.

El registro contiene un hash compatible con Argon2:

```text
$argon2id$...
```

### Login correcto

Se realizó autenticación con las credenciales correctas.

La operación devolvió un token JWT.

La respuesta contiene:

```text
token
tokenType
user
```

### Login incorrecto

Se realizó una prueba utilizando credenciales incorrectas.

La API respondió:

```text
Credenciales incorrectas
```

Esto confirma que las credenciales inválidas son rechazadas.

### Crear usuario de empresa

Utilizando el JWT obtenido mediante `login`, se creó correctamente un usuario asociado a la empresa.

Datos utilizados:

```text
Nombre: Usuario Demo
Correo: usuario@demo.com
```

El registro generado presentó:

```text
isAdmin = false
isActive = true
```

### Consultar usuarios de una empresa

Se ejecutó:

```graphql
query {
  companyUsers(companyId: "1") {
    id
    companyId
    userId
    isAdmin
    isActive
    joinedAt
    company {
      id
      name
    }
    user {
      id
      name
      email
    }
  }
}
```

La respuesta permitió comprobar las relaciones entre:

```text
CompanyUser
Company
User
```

### Desactivar usuario

Se ejecutó:

```graphql
mutation {
  deactivateCompanyUser(id: "2") {
    id
    companyId
    userId
    isAdmin
    isActive
  }
}
```

El resultado confirmó:

```text
isActive = false
```

La desactivación se aplicó a la relación `CompanyUser`.

El usuario global permaneció registrado.

## 19. Pruebas de validaciones

También se realizaron pruebas específicas para validar las reglas de negocio.

### Correo duplicado

Se intentó registrar nuevamente:

```text
usuario@demo.com
```

La API respondió:

```text
El correo electrónico ya está registrado
```

### Segundo administrador

Se intentó crear un segundo administrador para la misma empresa.

La API respondió:

```text
La empresa ya tiene un administrador principal
```

Esto confirma la regla de un solo administrador principal por empresa.

### Empresa inexistente

Se intentó crear una relación utilizando:

```text
companyId = 9999
```

La API respondió:

```text
La empresa no existe
```

### Correo electrónico inválido

Se realizó una prueba utilizando un correo con formato incorrecto.

La API respondió:

```text
El correo electrónico no es válido
```

## 20. Manejo de errores

Las operaciones de negocio contienen validaciones antes de realizar cambios en la base de datos.

Entre las situaciones controladas se encuentran:

```text
Empresa inexistente
Empresa inactiva
Usuario inexistente
Usuario inactivo
Correo duplicado
Correo inválido
Segundo administrador
Usuario sin permisos administrativos
Credenciales incorrectas
Relación Empresa–Usuario inexistente
```

También se controla `IntegrityError` de SQLAlchemy en las operaciones donde existe riesgo de violar restricciones de la base de datos.

## 21. Organización de servicios

La lógica de negocio se distribuye en diferentes servicios.

### CompanyService

Gestiona las operaciones relacionadas con las empresas:

```text
Crear empresa
Actualizar empresa
Consultar empresa
Listar empresas
Desactivar empresa
```

### UserService

Gestiona los usuarios:

```text
Crear usuario
Buscar usuario
Actualizar usuario
Validar correo
Verificar contraseña
Generar hash
```

### AuthService

Gestiona la autenticación:

```text
Login
Verificación de credenciales
Generación de JWT
```

### CompanyUserService

Gestiona la relación entre empresas y usuarios:

```text
Crear administrador
Crear usuario de empresa
Consultar usuarios de empresa
Desactivar usuario de empresa
Validar permisos administrativos
```

## 22. Seguridad

Las principales medidas implementadas son:

- Hash de contraseñas mediante Argon2.
- Validación y normalización de correos electrónicos.
- Autenticación mediante JWT.
- Expiración configurable del token.
- Validación del usuario autenticado.
- Verificación de usuarios activos.
- Control de permisos administrativos.
- Restricción de un administrador principal por empresa.
- Variables sensibles mediante `.env`.

## 23. Flujo completo de autenticación

El funcionamiento general del sistema puede representarse de la siguiente manera:

```text
1. Crear administrador
        |
        v
2. Guardar usuario
        |
        v
3. Generar hash Argon2
        |
        v
4. Crear relación CompanyUser
        |
        v
5. Login
        |
        v
6. Validar correo y contraseña
        |
        v
7. Generar JWT
        |
        v
8. Enviar Bearer Token
        |
        v
9. Crear o administrar usuarios
        |
        v
10. Validar permisos
        |
        v
11. Ejecutar operación
```

## 24. Flujo de creación de usuarios

El administrador principal puede crear usuarios dentro de su empresa.

```text
Administrador autenticado
          |
          v
       JWT
          |
          v
createCompanyUser
          |
          v
Validar token
          |
          v
Buscar empresa
          |
          v
Verificar administrador
          |
          v
Validar correo
          |
          v
Crear usuario
          |
          v
Generar hash Argon2
          |
          v
Crear CompanyUser
          |
          v
Usuario creado
```

## 25. Git y control de versiones

El proyecto se encuentra versionado mediante Git.

Repositorio:

```text
https://github.com/Dave2826/actividad4-david-morales.git
```

La rama principal utilizada es:

```text
main
```

Los commits principales realizados durante la actividad son:

```text
21bf204 feat: implementar CRUD de empresas con GraphQL
1f1c93e feat: implementar usuarios autenticacion y administracion
1809bd1 feat: implementar gestion de usuarios por empresa
ab06187 feat: completar gestion de usuarios y relaciones
```

El último commit contiene la implementación completa de la gestión de usuarios y relaciones entre empresas y usuarios.

Estado final del repositorio:

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

## 26. Resultado final

Al finalizar la actividad, el backend permite gestionar empresas, usuarios y las relaciones entre ambos mediante GraphQL.

Las principales funcionalidades implementadas son:

```text
CRUD de empresas
        +
Gestión de usuarios
        +
Relación Empresa–Usuario
        +
Administrador principal
        +
Usuarios de empresa
        +
Autenticación
        +
JWT
        +
Hash Argon2
        +
Validación de correo
        +
Control de permisos
        +
Desactivación de usuarios
        +
Consultas GraphQL
        +
Docker
        +
PostgreSQL
```

El sistema permite mantener una separación entre la información global del usuario y su participación dentro de una empresa.

La entidad `CompanyUser` permite controlar si un usuario es administrador, si su relación está activa y cuándo se incorporó a la empresa.

Además, la combinación de validaciones en la lógica de negocio y restricciones en PostgreSQL permite mantener las reglas principales de integridad del sistema.

## 27. Conclusión

En esta actividad se implementó la relación entre empresas y usuarios mediante una estructura que permite administrar diferentes usuarios dentro de una empresa y distinguir al administrador principal de los usuarios normales.

La implementación permitió integrar diferentes componentes del backend, incluyendo FastAPI, GraphQL, SQLAlchemy, PostgreSQL, Alembic y Docker. También se incorporó autenticación mediante JWT y protección de contraseñas utilizando Argon2.

Uno de los puntos principales fue establecer la regla de que cada empresa solamente puede contar con un administrador principal. Esta regla no depende únicamente de una validación en el código, ya que también se estableció una restricción en PostgreSQL para mantener la integridad de los datos.

Las pruebas realizadas permitieron comprobar la creación del administrador, creación de usuarios, autenticación correcta e incorrecta, validación de correos, prevención de correos duplicados, prevención de un segundo administrador, validación de empresas inexistentes y desactivación de relaciones Empresa–Usuario.

Con esto se completó la implementación solicitada para la gestión de usuarios y su relación con las empresas dentro del backend.

## 28. Autor

**David Morales Guerrero**

Tecnológico del Software

TSU en Desarrollo e Innovación de Software

Actividad 4 - Fundamentos de Arquitectura de Software y Desarrollo Backend