import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./App.css";
import { AppContext } from "./context/AppContext";

import { RegisterData, NewCupcakeData } from "./types";

import useLocalStorage from "./hooks/useLocalStorage";

import KupacakesAPI from "./kupacakesAPI";

const App = () => {
  const [token, setToken] = useLocalStorage("token");
  const [userId, setUserId] = useLocalStorage("userId");

  const [isLoading, setIsLoading] = useState(true);
  const [errors, setErrors] = useState<string[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    const checkToken = async () => {
      setIsLoading(true);
      try {
        if (token) {
          KupacakesAPI.loadApi(token as string);
        }
      } catch (errors) {
        setErrors(errors as string[]);
      }
      setIsLoading(false);
    };
    checkToken();
  }, [token]);

  const handleLogin = async (data: { username: string; password: string }) => {
    setIsLoading(true);
    try {
      const { token, userId } = await KupacakesAPI.login(data);
      setToken(token);
      setUserId(userId);
    } catch (errors) {
      setErrors(errors as string[]);
    }
    setIsLoading(false);
  };

  const handleLogout = async () => {
    setIsLoading(true);
    try {
      await KupacakesAPI.logout();
      setUserId(null);
      setToken(null);
    } catch (errors) {
      setErrors(errors as string[]);
    }
    setIsLoading(false);
  };

  const handleRegister = async (data: RegisterData) => {
    setIsLoading(true);
    try {
      const { token, userId } = await KupacakesAPI.register(data);
      setToken(token);
      setUserId(userId);
    } catch (errors) {
      setErrors(errors as string[]);
    }
    setIsLoading(false);
  };

  const handleCreateCupcake = async (data: NewCupcakeData) => {
    setIsLoading(true);
    try {
      const cupcake = await KupacakesAPI.generateCupcake(data);
      setIsLoading(false);
      navigate(`/cupcakes/${cupcake.id}`);
    } catch (errors) {
      setErrors(errors as string[]);
      setIsLoading(false);
    }
  };

  const handleGetCupcake = async (id: number) => {
    setIsLoading(true);
    try {
      const cupcake = await KupacakesAPI.getCupcake(id);
      setIsLoading(false);
      return cupcake;
    } catch (errors) {
      setErrors(errors as string[]);
      setIsLoading(false);
    }
  };

  const handleGetCupcakes = async (userId: number | null = null) => {
    setIsLoading(true);
    try {
      const cupcakes = await KupacakesAPI.getCupcakes(userId);
      setIsLoading(false);
      return cupcakes;
    } catch (errors) {
      setErrors(errors as string[]);
      setIsLoading(false);
    }
  };

  const handleDeleteCupcake = async (id: number) => {
    setIsLoading(true);
    try {
      await KupacakesAPI.deleteCupcake(id);
      setIsLoading(false);
      navigate("/cupcakes");
    } catch (errors) {
      setErrors(errors as string[]);
      setIsLoading(false);
    }
  };

  return (
    <AppContext.Provider
      value={{
        userId,
        isLoading,
        errors,
        handleLogin,
        handleLogout,
        handleRegister,
        handleCreateCupcake,
        handleGetCupcake,
        handleGetCupcakes,
        handleDeleteCupcake,
      }}
    >
      <div className="App">
        <header className="App-header">
          <h1>KupaCakes</h1>
        </header>
      </div>
    </AppContext.Provider>
  );
};

export default App;
