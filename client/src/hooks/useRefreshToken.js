import { useAuth } from "../context/AuthContext";
import api from "../api/axios";

export default function useRefreshToken() {
    const { login } = useAuth();

    const refresh = async () => {
        const res = await api.get("/auth/refresh");
        login(res.data);
        return res.data.accessToken;
    }

    return refresh;
}