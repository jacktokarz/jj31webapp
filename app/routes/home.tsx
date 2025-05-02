import type { Route } from "./+types/home";
import { Welcome } from "../welcome/welcome";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "JJ Bday :)" },
    { name: "error", content: "Oops, you shouldn't see this page!" },
  ];
}

export default function Home() {
  return <Welcome />;
}
