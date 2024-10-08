import { RiOpenaiFill } from "react-icons/ri";
import { FcGoogle } from "react-icons/fc";
import anthropic from "../images/anthropic.svg";
import perplexity from "../images/perplexity.png";
import mistral from "../images/mistral.svg";
import meta from "../images/meta.svg";

export const modelOptions = [
    { label: "GPT-3.5 Turbo", value: "gpt-3.5-turbo", companyLogo: <RiOpenaiFill />, color: "text-blue-500", isPremium: false },
    { label: "GPT-4 Turbo Preview", value: "gpt-4-turbo-preview", companyLogo: <RiOpenaiFill />, color: "text-blue-500", isPremium: true },
    { label: "GPT-4o", value: "gpt-4o", companyLogo: <RiOpenaiFill />, color: "text-blue-500", isPremium: true },
    { label: "GPT-4 o mini", value: "gpt-4o-mini", companyLogo: <RiOpenaiFill />, color: "text-blue-500", isPremium: false },
    { label: "Claude 3 Haiku", value: "claude-3-haiku-20240307", companyLogo: <img src={anthropic} alt="" width={20} height={20} />, color: "text-orange-300", isPremium: false },
    { label: "Claude 3 Sonnet", value: "claude-3-sonnet-20240229", companyLogo: <img src={anthropic} alt="" width={20} height={20} />, color: "text-orange-300", isPremium: true },
    { label: "Claude 3 Opus", value: "claude-3-opus-20240229", companyLogo: <img src={anthropic} alt="" width={20} height={20} />, color: "text-orange-300", isPremium: true },
    { label: "Claude 3.5 Sonnet", value: "claude-3-5-sonnet-20240620", companyLogo: <img src={anthropic} alt="" width={20} height={20} />, color: "text-orange-300", isPremium: true },
    { label: "Mistral Tiny", value: "mistral-tiny-2312", companyLogo: <img src={mistral} alt="" width={20} height={20} />, color: "text-orange-600", isPremium: false },
    { label: "Mistral Small", value: "mistral-small-2312", companyLogo: <img src={mistral} alt="" width={20} height={20} />, color: "text-orange-600", isPremium: false },
    { label: "Mistral Small Latest", value: "mistral-small-2402", companyLogo: <img src={mistral} alt="" width={20} height={20} />, color: "text-orange-600", isPremium: false },
    { label: "Mistral Medium Latest", value: "mistral-medium-2312", companyLogo: <img src={mistral} alt="" width={20} height={20} />, color: "text-orange-600", isPremium: true },
    { label: "Mistral Large Latest", value: "mistral-large-2402", companyLogo: <img src={mistral} alt="" width={20} height={20} />, color: "text-orange-600", isPremium: true },
    { label: "Gemini 1.0 Pro", value: "gemini-1.0-pro", companyLogo: <FcGoogle />, color: "text-google-gradient", isPremium: false },
    { label: "Gemini 1.5 Flash", value: "gemini-1.5-flash-latest", companyLogo: <FcGoogle />, color: "bg-google-gradient", isPremium: false },
    { label: "Gemini 1.5 Pro", value: "gemini-1.5-pro-latest", companyLogo: <FcGoogle />, color: "bg-google-gradient", isPremium: true },
    { label: "Gemma 2b", value: "google/gemma-2b-it", companyLogo: <FcGoogle />, color: "bg-google-gradient", isPremium: false },
    { label: "Gemma 7b", value: "google/gemma-7b-it", companyLogo: <FcGoogle />, color: "bg-google-gradient", isPremium: false },
    { label: "Sonar Small 32k Online", value: "llama-3-sonar-small-32k-online", companyLogo: <img src={perplexity} alt="" width={20} height={20} />, color: "text-blue-500", isPremium: false },
    { label: "Sonar Small 32k Chat", value: "llama-3-sonar-small-32k-chat", companyLogo: <img src={perplexity} alt="" width={20} height={20} />, color: "text-blue-500", isPremium: true },
    { label: "Sonar Large 32k Online", value: "llama-3-sonar-large-32k-online", companyLogo: <img src={perplexity} alt="" width={20} height={20} />, color: "text-blue-500", isPremium: false },
    { label: "Sonar Large 32k Chat", value: "llama-3-sonar-large-32k-chat", companyLogo: <img src={perplexity} alt="" width={20} height={20} />, color: "text-blue-500", isPremium: true },
    { label: "Sonar Small 128k Online", value: "llama-3.1-sonar-small-128k-online", companyLogo: <img src={perplexity} alt="" width={20} height={20} />, color: "text-blue-500", isPremium: true },
    { label: "Sonar Small 128k Chat", value: "llama-3.1-sonar-small-128k-chat", companyLogo: <img src={perplexity} alt="" width={20} height={20} />, color: "text-blue-500", isPremium: true },
    { label: "Sonar Large 128k Online", value: "llama-3.1-sonar-large-128k-online", companyLogo: <img src={perplexity} alt="" width={20} height={20} />, color: "text-blue-500", isPremium: true },
    { label: "Sonar Large 128k Chat", value: "llama-3.1-sonar-large-128k-chat", companyLogo: <img src={perplexity} alt="" width={20} height={20} />, color: "text-blue-500", isPremium: true },
    { label: "Codellama 34b Instruct", value: "codellama/CodeLlama-34b-Instruct-hf", companyLogo: <img src={meta} alt="" width={20} height={20} />, color: "text-blue-500", isPremium: false },
    { label: "Codellama 70b Instruct", value: "codellama/CodeLlama-70b-Instruct-hf", companyLogo: <img src={meta} alt="" width={20} height={20} />, color: "text-blue-500", isPremium: true },
    { label: "Meta Llama 2 13b Chat", value: "meta-llama/Llama-2-13b-chat-hf", companyLogo: <img src={meta} alt="" width={20} height={20} />, color: "text-blue-500", isPremium: false },
    { label: "Meta Llama 2 70b Chat", value: "meta-llama/Llama-2-70b-chat-hf", companyLogo: <img src={meta} alt="" width={20} height={20} />, color: "text-blue-500", isPremium: true },
    { label: "Meta Llama 3 8b Chat", value: "meta-llama/Llama-3-8b-chat-hf", companyLogo: <img src={meta} alt="" width={20} height={20} />, color: "text-blue-500", isPremium: false },
    { label: "Meta Llama 3 70b Chat", value: "meta-llama/Llama-3-70b-chat-hf", companyLogo: <img src={meta} alt="" width={20} height={20} />, color: "text-blue-500", isPremium: true },
    { label: "Meta Llama 3.1 8B Instruct Turbo", value: "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo", companyLogo: <img src={meta} alt="" width={20} height={20} />, color: "text-blue-500", isPremium: true },
    { label: "Meta Llama 3.1 70B Instruct Turbo", value: "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo", companyLogo: <img src={meta} alt="" width={20} height={20} />, color: "text-blue-500", isPremium: true },
    { label: "Meta Llama 3.1 405B Instruct Turbo", value: "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo", companyLogo: <img src={meta} alt="" width={20} height={20} />, color: "text-blue-500", isPremium: true },
];
