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
  background: linear-gradient(135deg, #ffeb3b, #ff7043);
  border: 3px solid #d32f2f; 
  border-radius: 20px;
  box-shadow: 0 5px 20px rgba(211, 47, 47, 0.3);
  padding: 20px;
  color: #212121;
  text-align: center;
  margin: 20px auto;
}

h1 {
  font-size: 2rem;
  margin-bottom: 20px;
  color: #c62828; 
  font-weight: bold;
}

button {
  background: linear-gradient(45deg, #ff7043, #e53935); 
  color: white;
  padding: 12px 30px;
  border: none;
  border-radius: 30px;
  font-size: 1rem;
  cursor: pointer;
  margin: 10px 0;
  transition: transform 0.3s ease, background 0.3s ease;
  box-shadow: 0 5px 12px rgba(229, 57, 53, 0.3);
}

button:hover {
  background: linear-gradient(45deg, #b71c1c, #c62828); 
  transform: scale(1.05);
  box-shadow: 0 8px 20px rgba(183, 28, 28, 0.5);
}

.message-box, .response-box {
  background: linear-gradient(135deg, #ffcc80, #ef5350);
  padding: 20px;
  border-radius: 15px;
  margin-top: 20px;
  text-align: left;
  width: 85%;
  max-width: 700px;
  color: #4e342e; 
  font-size: 1.1rem;
  font-weight: bold;
  line-height: 1.6;
  word-wrap: break-word;
  white-space: pre-wrap;
  box-shadow: 0 4px 8px rgba(255, 87, 87, 0.3);
  margin-bottom: 30px;
}

.message-box h2, .response-box h2 {
  margin-bottom: 12px;
  font-size: 1.4rem;
  color: #d32f2f;
  text-transform: uppercase;
}

.message-box p, .response-box p {
  color: #6d4c41; 
  font-size: 1rem;
}

.loading-box {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 85%;
  max-width: 700px;
  padding: 20px;
  margin-top: 20px;
  background: linear-gradient(135deg, #ff7043, #d32f2f); 
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(211, 47, 47, 0.4); 
  color: white;
  font-size: 1.3rem;
  font-weight: bold;
  text-align: center;
  animation: pulse 1.5s infinite;
}

.loading-box p {
  margin: 0;
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 0.9;
  }
  50% {
    transform: scale(1.05);
    opacity: 1;
  }
  100% {
    transform: scale(1);
    opacity: 0.9;
  }
}
</style>
