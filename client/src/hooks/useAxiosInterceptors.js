import { useEffect } from 'react';
import api from '../api/axios';
import useRefreshToken from './useRefreshToken';
import { useAuth } from '../context/AuthContext';

const useAxiosInterceptors = () => {
  const refresh = useRefreshToken();
  const { user } = useAuth(); // Assumes useAuth exposes your user state containing the accessToken

  useEffect(() => {
    const requestIntercept = api.interceptors.request.use(
      (config) => {
        if (!config.headers['Authorization']) {
          config.headers['Authorization'] = `Bearer ${user?.accessToken}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    const responseIntercept = api.interceptors.response.use(
      (response) => response,
      async (error) => {
        const prevRequest = error?.config;
        if (error?.response?.status === 401 && !prevRequest?.sent) {
          prevRequest.sent = true; // Prevents infinite loops if the refresh token is also invalid
          const newAccessToken = await refresh();
          prevRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;
          return api(prevRequest);
        }
        return Promise.reject(error);
      }
    );

    return () => {
      api.interceptors.request.eject(requestIntercept);
      api.interceptors.response.eject(responseIntercept);
    };
  }, [user, refresh]);

  return api;
};

export default useAxiosInterceptors;
