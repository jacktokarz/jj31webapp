import type { Route } from "./+types/home";
import { Welcome } from "../welcome/welcome";
import { QuestionStore } from "../welcome/QuestionStore";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "JJ Bday :)" },
    { name: "error", content: "Oops, you shouldn't see this page!" },
  ];
}

export function QuestionPage() {
	return <QuestionStore />;
}

export default function Home() {
  return <Welcome />;
}
