import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

export const generateContent = async (contentData) => {
  try {
    console.log("Sending request to API:", contentData);
    const response = await axios.post(`${API_URL}/generate-content`, contentData);
    console.log("Received response:", response.data);
    return response.data;
  } catch (error) {
    console.error('Error generating content:', error);
    throw error;
  }
};

export default {
  generateContent
};
