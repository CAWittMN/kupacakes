// JWT payload type
type JwtPayload = {
  token_type: string;
  exp: number;
  iat: number;
  jti: string;
  user_id: number;
};

type RegisterData = {
  username: string;
  password: string;
  first_name: string;
  last_name: string;
  email: string;
};

type NewCupcakeData = {
  key_ingredients: string[];
  description: string;
  stupid_article: boolean;
};

type ContextProvider = {
  children: React.ReactNode;
};

export type { JwtPayload, RegisterData, NewCupcakeData, ContextProvider };
