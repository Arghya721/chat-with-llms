import React, { useState, useMemo } from 'react';
import { Card, CardBody, CardFooter } from "@nextui-org/react";
import { AiOutlineCopy, AiOutlineCheck } from 'react-icons/ai';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { okaidia } from 'react-syntax-highlighter/dist/esm/styles/prism';

export const AiCard = ({ message, retryComponent }) => {
  const [copied, setCopied] = useState(false);
  const [codeToCopy, setCodeToCopy] = useState('');

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(message);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000); // Reset the copied state after 2 seconds
    } catch (error) {
      console.error('Failed to copy:', error);
    }
  };

  const handleCodeCopy = async (code) => {
    try {
      await navigator.clipboard.writeText(code);
      setCodeToCopy(code);
      setTimeout(() => setCodeToCopy(''), 2000); // Reset the codeToCopy state after 2 seconds
    } catch (error) {
      console.error('Failed to copy code:', error);
    }
  };

  const renderedMarkdown = useMemo(() => (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      children={message}
      components={{
        code({ children, className, node, ...rest }) {
          const match = /language-(\w+)/.exec(className || '');
          const code = String(children).replace(/\n$/, '');
          return match ? (
            <div className="relative">
              <SyntaxHighlighter
                {...rest}
                PreTag="div"
                children={code}
                language={match[1]}
                style={okaidia}
              />
              <button
                className={`absolute top-2 right-2 flex items-center gap-2 p-2 rounded transition duration-300 ease-in-out dark:text-gray-400 dark:hover:text-white text-gray-600 hover:text-gray-800`}
                onClick={() => handleCodeCopy(code)}
              >
                {codeToCopy === code ? (
                  <>
                    <AiOutlineCheck className="text-green-600" />
                    <span className="text-green-600">Copied</span>
                  </>
                ) : (
                  <>
                    <AiOutlineCopy />
                    <span>Copy Code</span>
                  </>
                )}
              </button>
            </div>
          ) : (
            <code {...rest} className={className}>
              {children}
            </code>
          );
        },
      }}
    />
  ), [message, codeToCopy]); // Memoize based on the message and codeToCopy

  const renderedCopyButton = useMemo(() => (
    <button
      className={`flex items-center gap-2 dark:text-gray-400 dark:hover:text-white text-gray-600 hover:text-gray-800 p-2 rounded transition duration-300 ease-in-out`}
      onClick={handleCopy}
    >
      {copied ? (
        <>
          <AiOutlineCheck className="text-green-600" />
          <span className="text-green-600">Copied</span>
        </>
      ) : (
        <>
          <AiOutlineCopy />
          <span>Copy</span>
        </>
      )}
    </button>
  ), [copied]); // Memoize the copy button based on the copied state

  return (
    <Card className={`max-w-max dark:bg-gray-700 dark:text-gray-200 bg-white text-gray-800`}>
      <CardBody>
        {renderedMarkdown}
      </CardBody>
      <CardFooter className="flex justify-end items-center p-2">
        {retryComponent}
        {renderedCopyButton}
      </CardFooter>
    </Card>
  );
};
