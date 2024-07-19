import { useState, useEffect } from "react";

const useLocalStorage = (key: string, firstValue: string | null = null) => {
  const initialValue = localStorage.getItem(key) || firstValue;
  const [item, setItem] = useState<string | null | number>(initialValue);

  useEffect(() => {
    if (!item) {
      localStorage.removeItem(key);
    } else {
      localStorage.seItem(key, item);
    }
  }, [item, key]);

  return [item, setItem] as const;
};

export default useLocalStorage;
