import { API_URL } from "@/constants";
import axios from "axios";
import { AxiosResponse, AxiosInstance } from "axios";
import { camelizeKeys, decamelizeKeys } from "humps";

export const axiosService: AxiosInstance = axios.create({
    baseURL: `${API_URL}/api`,
    withCredentials: false,
});

// Request interceptor
axiosService.interceptors.request.use((config) => {
    if (config.data && !(config.data instanceof FormData)) {
        config.data = decamelizeKeys(config.data);
    }
    return config;
});

// Response interceptor
axiosService.interceptors.response.use(
    (response: AxiosResponse) => {
        if (response.data) {
            response.data = camelizeKeys(response.data);
        }
        return response;
    },

    async (error) => {
        // Response interceptor
        axiosService.interceptors.response.use(
            (response: AxiosResponse) => {
                if (response.data) {
                    response.data = camelizeKeys(response.data);
                }
                return response;
            },
            async (error) => {
                if (error.response && error.response.data) {
                    error.response.data = camelizeKeys(error.response.data);
                }

                return Promise.reject(error);
            }
        );

        if (error.response && error.response.data) {
            error.response.data = camelizeKeys(error.response.data);
        }

        return Promise.reject(error);
    }
);
