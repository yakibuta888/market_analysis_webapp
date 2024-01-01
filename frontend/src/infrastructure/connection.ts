import mysql from 'mysql2/promise'

export async function connectMySQL() {
  return await mysql.createConnection({
    host: 'mysql',
    database: 'reversi',
    user: 'reversi',
    password: 'password'
  })
}
