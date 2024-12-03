<template>
  <div id="app">
    
    <router-view></router-view>
  </div>
</template>

<style>
#app {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  width: 80%;
  max-width: 900px;
  height: 100%;
  background: linear-gradient(90deg, #ff007f, #7f00ff);
  border: 5px solid #ff007f;
  border-radius: 20px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.5);
  padding: 20px;
  color: white;
  text-align: center;
  margin: 20px auto;
}

h1 {
  font-size: 2rem;
  margin-bottom: 20px;
  color: #ffeb3b;
}

button {
  background: linear-gradient(45deg, #00ff7f, #00e5ff);
  color: white;
  padding: 12px 30px;
  border: none;
  border-radius: 30px;
  font-size: 1.2rem;
  cursor: pointer;
  margin: 10px 0;
  transition: transform 0.3s ease, background 0.3s ease;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

button:hover {
  background: linear-gradient(45deg, #ff007f, #ff4500);
  transform: scale(1.1);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5);
}

button[v-if="mensaje"] {
  background: linear-gradient(45deg, #ff5722, #ff9100);
}

button[v-if="mensaje"]:hover {
  background: linear-gradient(45deg, #ff6a00, #e65100);
}

.message-box, .response-box {
  background: linear-gradient(45deg, #ff00ff, #8000ff);
  padding: 20px;
  border-radius: 15px;
  margin-top: 20px;
  text-align: left;
  width: 85%;
  max-width: 700px;
  color: white;
  font-size: 1.2rem;
  font-weight: 500;
  line-height: 1.6;
  word-wrap: break-word;
  white-space: pre-wrap;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  margin-bottom: 30px;
}

.message-box h2, .response-box h2 {
  margin-bottom: 12px;
  font-size: 1.5rem;
  color: #fff700;
  text-transform: uppercase;
}

.message-box p, .response-box p {
  color: #e0e0e0;
  font-size: 1.1rem;
}

.message-box, .response-box {
  max-height: none; 
  overflow: visible;
}

</style>
