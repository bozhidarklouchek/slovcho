import axios from 'axios';

export const classifyStyle =  async (rawText) => {
    try {
      const response = await axios.post('http://localhost:5000/classify_style', {
        function_name: 'classify_style',
        parameter: rawText
      });

      return (response.data.output.replace(/\n/g, ''));
    } catch (error) {
      console.error('Error calling Python function:', error);
    }
  };

export const spellCheck =  async (processedSents) => {
    try {
      console.log('here is what i sent', processedSents)
      const response = await axios.post('http://localhost:5000/spell_check', {
        parameter: processedSents
      });
      console.log('here is what i receive', response)
      return (response.data.output.flat())

    } catch (error) {
      console.error('Error calling Python function:', error);
    }
  };

  export const grammarCheck =  async (sents) => {
    try {
      const response = await axios.post('http://localhost:5000/grammar_check', {
        parameter: sents
      });
      return (response.data.output)

    } catch (error) {
      console.error('Error calling Python function:', error);
    }
  };

export const preprocessInput = async (text) => {
    try {
      const response = await axios.post('http://localhost:5000/preprocess_input', {
        parameter: text
      });

      return response.data.output
    } catch (error) {
      console.error('Error calling Python function:', error);
    }
  }


  export const getWordPos = async (word) => {
    try {
      const response = await axios.post('http://localhost:5000/get_word_pos', {
        parameter: word
      });

      return response.data.output
    } catch (error) {
      console.error('Error calling Python function:', error);
    }
  }