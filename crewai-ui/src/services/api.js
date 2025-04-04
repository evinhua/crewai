import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

export const generateContent = async (contentData) => {
  try {
    const response = await axios.post(`${API_URL}/generate-content`, contentData);
    return response.data;
  } catch (error) {
    console.error('Error generating content:', error);
    throw error;
  }
};

export default {
  generateContent
};
