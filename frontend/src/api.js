import axios from "axios";

// Create a reusable API instance pointing to Flask backend
const API = axios.create({
  baseURL: "http://localhost:5001", // Flask backend port
});

export const uploadImage = async (image) => {
  if (!image) throw new Error("No image provided");

  const formData = new FormData();
  formData.append("image", image);

  const res = await API.post("/detect", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return res.data; // return the detection results
};
