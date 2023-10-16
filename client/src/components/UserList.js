import React from 'react'

function UserList(props) {
  return (
    <div>
      {props.users && props.users.map(user => {
        return (
          <div key = {user.id}>
            <h2>{user.nick}</h2>
            <p>{user.email}</p>
          </div>
        )
      })}
    </div>
  )
}

export default UserList
