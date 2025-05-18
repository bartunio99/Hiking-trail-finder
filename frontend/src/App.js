import React, { useState } from 'react';

function App() {

  const API_URL = process.env.REACT_APP_API_URL;
  const [name, setName] = useState('');
  const [radius, setRadius] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    const place = {
      name: name,
      radius: parseFloat(radius),
    };

    try {
      const response = await fetch(`${API_URL}/map/places/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(place),
      });

      const data = await response.json();
      console.log('Place submitted:', data);
    } catch (error) {
      console.error('Error submitting place:', error);
    }
  };

const handleGenerateMap = async () => {
  const place = {
    name: name,
    radius: parseFloat(radius),
  };

  try {
    const response = await fetch(`${API_URL}/map/places/maps/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(place),
    });

    // Get the response as a Blob (binary data)
    const blob = await response.blob();

    // Create a blob URL from the response
    const url = URL.createObjectURL(blob);

    // Open the blob URL in a new tab
    window.open(url, '_blank');
  } catch (error) {
    console.error('Error generating map:', error);
  }
};


  return (
    <div className="App" style={{ padding: '30px' }}>
      <h1 style={{ textAlign: 'center' }}> Search hiking trails</h1>

      <div style={{ textAlign: 'left' }}>
        <p>Please enter the place name and search radius below:</p>
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

        {/* New "Generate Map" button */}
        <div style={{ marginTop: '20px' }}>
          <button onClick={handleGenerateMap}>Generate Map</button>
        </div>
      </div>
    </div>
  );
}

export default App;
