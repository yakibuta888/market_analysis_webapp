import { useState } from "react";

const TextInput = () => {
  const [text, setText] = useState<string>('');
  return (
    <div>
      <input
        type="text"
        onChange={(e) => setText(e.target.value)}
        value={text}
        placeholder="Type something here..."
      />
      <p>{text}</p>
    </div>
  );
};

export default TextInput;
