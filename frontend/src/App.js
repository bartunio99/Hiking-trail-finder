// App.js
import React, { useState } from 'react';

function App() {
  const [name, setName] = useState('');
  const [radius, setRadius] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    const place = {
      name: name,
      radius: parseFloat(radius),
    };

    try {
      const response = await fetch('http://localhost:3001/map/places/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(place),
      });

      const data = await response.json();
      console.log('Success:', data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="App">
      <form onSubmit={handleSubmit}>
        <div>
          <label>Place Name:</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Radius:</label>
          <input
            type="number"
            step="any"
            value={radius}
            onChange={(e) => setRadius(e.target.value)}
            required
          />
        </div>
        <button type="submit">Submit Place</button>
      </form>
    </div>
  );
}

export default App;
