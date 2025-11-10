import axios from "axios";
import Cookies from "js-cookie";

const axiosClient = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL,
    headers: {
        "Content-Type": "application/json",
        "X-Api-Key": import.meta.env.VITE_FRONTEND_API_KEY
    },
})

axiosClient.interceptors.request.use(
    (config) => {
        const token = Cookies.get("access_token");
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        if (error.response?.status === 401) {
            Cookies.remove("access_token");
            window.location.href = "/login"; // Redirect to login page
        }
        return Promise.reject(error);
    }
)

export default axiosClient;