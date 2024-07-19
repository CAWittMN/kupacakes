import axios from "axios";
import { jwtDecode } from "jwt-decode";
import { JwtPayload, RegisterData, NewCupcakeData } from "./types";

const BASE_URL =
  import.meta.env.VITE_REACT_APP_API_URL || "http://localhost:3001";

class KupacakesAPI {
  static token: string | null = null;
  static userId: number | null = null;

  static async request(endpoint: string, data = {}, method = "get") {
    console.debug("API Call:", endpoint, data, method);

    const url = `${BASE_URL}/${endpoint}`;
    const headers = { Authorization: `Bearer ${this.token}` };
    const params = method === "get" ? data : {};

    try {
      return (await axios({ url, method, data, params, headers })).data;
    } catch (err: any) {
      console.error("API Error:", err.response);
      let message = err.response.data.error.message;
      throw Array.isArray(message) ? message : [message];
    }
  }

  static loadApi(token: string) {
    this.token = token;
    this.userId = jwtDecode<JwtPayload>(token).user_id;
    console.debug("KupaCakesAPI", "loaded", this.token, this.userId);
  }

  //Authentication API

  static async login(data: { username: string; password: string }) {
    let res = await this.request("auth/login", data, "post");
    const token: string = res.access;
    this.loadApi(token);
    return { token, userId: this.userId };
  }

  static async register(data: RegisterData) {
    let res = await this.request("auth/register", data, "post");
    const token = res.access;
    this.loadApi(token);
    return { token, userId: this.userId };
  }

  static async logout() {
    await this.request("auth/logout", {}, "post");
    this.token = null;
    this.userId = null;
  }

  // Cupcake API

  static async getCupcakes(userId: number | null = null) {
    const endpoint = userId ? "cupcakes/user/${userId}/" : "cupcakes/";
    return this.request(endpoint);
  }

  static async getCupcake(cupcakeId: number) {
    return this.request(`cupcakes/${cupcakeId}`);
  }

  static async generateCupcake(data: NewCupcakeData) {
    return this.request(`cupcakes/create/`, data, "post");
  }

  static async deleteCupcake(cupcakeId: number) {
    return this.request(`cupcakes/${cupcakeId}/`, {}, "delete");
  }

  static async updateCupcake(cupcakeId: number, data: NewCupcakeData) {
    return this.request(`cupcakes/${cupcakeId}/`, data, "patch");
  }
}

export default KupacakesAPI;
