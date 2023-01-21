import React, { useState, useEffect } from 'react'

function App() {
const [data, setData] = useState([{}]);

// Need to know what port the Flask API is attached to in order to finish POC
useEffect(() => {
  fetch("/something").then(
    res => res.json()
  ).then(
    data => {
      setData(data)
      console.log(data)
    }
  )
}, []);

return (
  <div>
    {(typeof data === 'undefined') ? (
        <p>Loading...</p>
    ) : (
      data.map((users, i) => (
        <p key={i}>
          {users}
        </p>
      ))
    )}

  </div>
)
}

export default App