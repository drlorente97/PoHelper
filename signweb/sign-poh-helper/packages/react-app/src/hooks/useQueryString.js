import {useLocation} from "react-router-dom"

export default function useQueryString() {
    const location = useLocation();
    return new URLSearchParams(location.search);
}