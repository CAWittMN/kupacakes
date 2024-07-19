import { createContext } from "react";
import { ContextProvider } from "../types";

export const AppContext = createContext<ContextProvider | undefined>(undefined);
