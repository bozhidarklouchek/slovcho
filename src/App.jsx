import React, { useState, useEffect, useRef} from "react";

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faGraduationCap, faHeart, faFaceLaughBeam, faGavel, faNewspaper } from '@fortawesome/free-solid-svg-icons';

import { classifyStyle, preprocessInput, spellCheck, getWordPos, grammarCheck } from "./Gateway";
import "./App.css";
import en from './assets/en.png';
import bg from './assets/bg.png';

function App() {

  const languageConstantsBG = {
    initialTitle: "Нека подобрим писането ти заедно.",
    updatedTitle: "Текстът е в {0} сфера.",
    textAreaPlaceholder: "Напиши нещо...",
    checkButton: "Провери стил",
    checkAgainButton: "Провери стил пак",
    wordCount: "Брой на думи: ",
    sentCount: "Брой на изречения: ",
    casual: "битовата",
    academic: "научната",
    news: "публицистичната",
    administrative: "институционалната",
    creative: "естетическата",
    styleLoading: "Изчакайте...",
    noCandidates: 'Няма предложения.'
  }

  const languageConstantsEN = {
    initialTitle: "Let's make your writing better together.",
    updatedTitle: "This text is written in the {0} style.",
    textAreaPlaceholder: "Type something...",
    checkButton: "Check style",
    checkAgainButton: "Check style again",
    wordCount: "Word count: ",
    sentCount: "Sentence count: ",
    casual: "casual",
    academic: "academic",
    news: "newswriting",
    administrative: "administrative",
    creative: "creative",
    styleLoading: "Loading...",
    noCandidates: 'No candidates.'
  }

  let languageConstants = null

  const realTextAreaRef = useRef(null); 

  const [isStyleLoading, setIsStyleLoading] = React.useState(false)
  const [isErrorLoading, setIsErrorLoading] = React.useState(false)

  const [language, setLanguage] = React.useState("bg")
  const [rawText, setRawText]= React.useState("")

  const [style, setStyle] = React.useState("")
  const [styleText, setStyleText] = React.useState("")
  const [styleTextStyleClass, setstyleTextStyleClass] = React.useState("")
  const [styleIcon, setStyleIcon] = React.useState(null)

  const [wordCount, setWordCount] = useState(0)
  const [processedSents, setProcessedSents] = useState([])

  const [spellCorrections, setSpellCorrections] = useState([])
  const [wordsWithCorrections, setWordsWithCorrections] = useState([])

  const [grammarCorrections, setGrammarCorrections] = useState([])
  const [grammarsThinking, setGrammarsThinking] = useState(0)

  const [suggestionWindow, setSuggestionWindow] = useState({
                                                            show: false,
                                                            top: -1,
                                                            left: -1,
                                                            wordOfInterest: '',
                                                            indexOfInterest: -1,
                                                            corrections: []
                                                          })
  // Possible options
  // creative
  // news
  // casual_real
  // academic_informal
  // administrative

  useEffect(() => {

    const updateWithNewInput = async () => {
      // Process input
      let processedTokens = await preprocessInput(rawText.replace(/[,\/#$%\^&\*;:{}=_`~()\[\]"'„“<>\\|]/g, ''))

      // Count all tokens that aren't punctuation as words
      setWordCount(processedTokens.filter((token) => token.pos != 'punct').length)

      // Save sentences
      let splitSentences = []
      let currSent = []
      processedTokens.forEach((token) => {
        if(token.is_sent_end && currSent.length !== 0)
        {
          currSent.push({text: token.text, pos: token.pos})
          splitSentences.push(currSent)
          currSent = []
        }
        else if(token.is_sent_start)
         {
           currSent.push({text: token.text, pos: token.pos})
         }
        else
        {
          currSent.push({text: token.text, pos: token.pos})
        }
      });
      splitSentences.forEach(sent => console.log('sent', sent.length))
      splitSentences.forEach(sent => sent.forEach(ch => console.log('sent', ch)))
      // let cleanedSents = splitSentences.map((sent) => sent.filter((token) => token.text !== '' && token.text !=='\n'))
      // console.log('аааа',cleanedSents)
      // setSentCount(cleanedSents.filter((sent) => sent.length > 1).length)
      setProcessedSents(splitSentences)
    };

    // Move caret in text area
    // moveCaretToEnd()
    if(rawText) updateWithNewInput();

  }, [rawText]);

  React.useEffect(() => {

    const fetchData = async () => {

      const styleDetails = style ?
          style == 'administrative'
          ? {description: languageConstants.administrative, icon: faGavel, style: "adm"}
          : style == 'academic_informal'
            ? {description:languageConstants.academic, icon: faGraduationCap, style: "acd"}
            : style == 'casual_real'
              ? {description:languageConstants.casual, icon: faFaceLaughBeam, style: "cas"}
              : style == 'creative'
                ? {description:languageConstants.creative, icon: faHeart, style: "crt"}
                : style == 'news'
                  ? {description:languageConstants.news, icon: faNewspaper, style: "news"}
                  : {description: null, iocn: null}
        : {description: null, icon: null}
      setStyleText(styleDetails.description)
      setStyleIcon(styleDetails.icon)
      setstyleTextStyleClass(styleDetails.style)
      
    };

    // Call the fetchData function when the component mounts
    fetchData();
  }, [style, language]);
  

  React.useEffect(() => {
    setIsErrorLoading(true)
    let ignore = false

    const fetchData = async () => {
      if(!ignore) setSpellCorrections(await spellCheck(processedSents.map((sent) => sent.filter((token) => token.pos != 'punct' && token.text != '\n' && token.text != '\n\n' ).map((word_pos) => word_pos.text))))
    }

    fetchData()

    return () => { ignore = true}
  }, [processedSents]);

  React.useEffect(() => {
    let ignore = false

    const fetchData = async () => {
      setGrammarsThinking(n => n + 1)
      let grammarCheckedText = await grammarCheck(processedSents.map((sent) => sent.map((word_pos) => word_pos.text)))
      
      setGrammarsThinking(n => n - 1)
      if(!ignore) setGrammarCorrections(grammarCheckedText.split(' '))
    }

    fetchData()

    return () => {ignore = true}
  }, [processedSents]);

  React.useEffect(() => {
    console.log('gram2', grammarCorrections)
  }, [grammarCorrections]);

  React.useEffect(() => {

    const fetchData = async () => {
      let processedTokens = processedSents.flat()
      console.log(processedSents)
      // Remove redundant tokens
      let word2correction = processedTokens.filter((token) => token.pos != 'punct' && token.text != '\n' && token.text != '\n\n' );
      console.log('zero filter', word2correction)
      console.log('spell filter', spellCorrections)
      word2correction = word2correction.map((token, index) => { return {text: token.text, pos: token.pos, correction: spellCorrections[index]}});
      console.log('initial filter', word2correction)
      // Remove correct tokens
      word2correction = word2correction.filter((token) => 
                                  token.correction &&
                                  (!token.correction[1] || (token.text[0] == token.text[0].toLowerCase())) &&
                                  ((token.correction[0].length != 1 ||
                                  (token.correction[0].length == 1 && token.correction[0][0][1] != 1))));
      console.log('second filter', word2correction)
      setWordsWithCorrections(word2correction)
      setIsErrorLoading(false)
    };

    // Call the fetchData function when the component mounts
    fetchData();
  }, [spellCorrections, grammarCorrections]);

  const languageButton = (language, path) => {
    return (
      <img onClick={() => setLanguage(language)}
           className="languageFlag"
           src={path}
           alt={language} />
    )
  }


  const renderWord = (isSpelledWrong, isGrammaticallyWrong, text, addSpace, corrections, wordIndex) => {
    return (
    <>
    {suggestionWindow.show && (
        <>
          <div className="candidateWindow" style={{
                       left: suggestionWindow.left,
                       top: suggestionWindow.top + 25
                       }}>
            {suggestionWindow.corrections.length !== 0
            ? suggestionWindow.corrections.map((candidate) => (
                <>
                  <span className='candidate' onClick={(e) => {
                            let newText = rawText.slice(0, suggestionWindow.indexOfInterest) + rawText.slice(suggestionWindow.indexOfInterest).replace(suggestionWindow.wordOfInterest, candidate)
                            realTextAreaRef.current.textContent = newText
                            setRawText(newText)
                            setSuggestionWindow({
                              show: false,
                              top: -1,
                              left: -1,
                              wordOfInterest: '',
                              corrections: []
                              })
                                        }}>
                    {candidate}
                  </span>
                  <br/>
                </>
                ))
            : <span className='candidate' onClick={(e) => {}}>
                {languageConstants.noCandidates}
              </span>}
          </div>
        </>
      )}
      <span
        className={isSpelledWrong
          ? 'littleSpanIsSpelledWrong'
          : grammarsThinking == 0 && isGrammaticallyWrong
          ? 'littleSpanIsGrammaticallyWrong'
          : 'littleSpanCorrect'}
        onClick={(e) => {
          console.log(text)
          if(suggestionWindow.show){
            setSuggestionWindow({
              show: false,
              top: -1,
              left: -1,
              wordOfInterest: '',
              indexOfInterest: -1,
              corrections: []
             })
          } else {
            setSuggestionWindow({
              show: true,
              top: e.currentTarget.getBoundingClientRect().top,
              left: e.currentTarget.getBoundingClientRect().left,
              wordOfInterest: text,
              indexOfInterest: wordIndex,
              corrections: corrections
            })
          }
        }}>
          {text}
          {addSpace ? <>&nbsp;</> : null}
      </span>
    </>
  )}

    const DotsBouncing = () => {
      return (
        <div className="dost-bouncing">
          <div className="dot-container">
            <div className="dot"></div>
            <div className="dot"></div>
            <div className="dot"></div>
          </div>
        </div>
      );
    }

    const Spinner = () => {
      return (
        <div className="spin-load">
          {/* You can use any kind of loading spinner or animation here */}
          <div className="spinner"></div>
        </div>
      );
    }
  

  const applySlovcho = async () => {
    setIsStyleLoading(true)

    // Classify style of writing
    setStyle(await classifyStyle(rawText))

    setIsStyleLoading(false)
  }

  languageConstants = language == 'en' ? languageConstantsEN : languageConstantsBG


  return (
    <div className="app">

      <div className="languageBox">
        {languageButton("en", en)}
        {languageButton("bg", bg)}
      </div>

      <div className="content">
        <div className="textColumn">
          <div className="textBox">
            <div
              id="real"
              ref={realTextAreaRef}
              className="input"
              contentEditable="plaintext-only"
              autoCorrect="false"
              onInput={(e) => {setRawText(e.currentTarget.textContent)}}
            >
            </div>
            
            <div
              id="dummy"
              className="input"
              autoCorrect="false"
              contentEditable="plaintext-only"
            > 
                {
                  
                  rawText.split('\n').join(' PARAGPRAPH_SYMBOL ').split(' ').map((rawWord, i) => {

                  let charIndex = 0
                  let splitText = rawText.split('\n').join(' PARAGPRAPH_SYMBOL ').split(' ')
                  for (let j = 0; j < splitText.length; j++) {
                    let word = splitText[j]
                    

                    if(i == j) break
                    if(word == 'PARAGPRAPH_SYMBOL')
                    {
                      charIndex--
                      break
                    }
                    for (let k = 0; k < word.length; k++) {
                      // Add one for each char of word
                      charIndex++
                    } 
                    // Add one for each space
                    charIndex++
                    }

                    let paragraphIndexBuffer = rawText.split('\n').join(' PARAGPRAPH_SYMBOL ').split(' ').slice(0, i + 1).filter(el => '' === el || 'PARAGPRAPH_SYMBOL' === el).length

                    let tempIndex = i - paragraphIndexBuffer

                    let cleanedWord = rawWord.replace(/[.,\/#!$%\^&\*;:{}=_`~()\[\]"'„“<>?\\|]/g, '')
                    let brokenWords = wordsWithCorrections.map((token) => token.text)

                    let corrections = []
                    let isSpelledWrong = false
                    let isGrammaticallyWrong = false
                    let grammarCheckedWord = grammarCorrections[tempIndex] != undefined
                      ? grammarCorrections[tempIndex].replace(/[.,\/#!$%\^&\*;:{}=_`~()\[\]"'„“<>?\\|]/g, '')
                      : ''

                    if(cleanedWord != grammarCheckedWord){
                      isGrammaticallyWrong = true
                    }
                    // console.log(i, cleanedWord, grammarCorrections[tempIndex])
                    
                    // If not only numerals in string and more than 2 chars
                    if(!/^[\d-]+$/.test(cleanedWord) && cleanedWord.length >= 3)
                    {
                      let count = 0;
                      for (let k = 0; k < brokenWords.length; k++) {
                          console.log(brokenWords[k])
                          console.log(cleanedWord)
                          if (brokenWords[k] === cleanedWord) {
                              corrections = wordsWithCorrections[k].correction[0].slice(0, 3).map((word_prob) => word_prob[0])
                              count++;
                          }
                      }
                      if(count >= 1) isSpelledWrong = true
                    }

                    // // If of type {numeral}-{adjective}
                    // if(!/\d+-[а-я]+$/.test(cleanedWord)){
                    //   // Check if alpha chars on the right are valid adj
                    //   console.log('got ittttt', getWordPos(cleanedWord.slice(cleanedWord.search('-') + 1)))
                    // }
                  

                    // Should only highlight word without non-alphanumertic chars after it
                    // if they are at the end or start
                    let leftIndex = 0
                    let rightIndex = rawWord.length
                    // console.log(/[^а-яА-Я0-9\s]/.test(rawWord), rawWord.slice(0))
                    if(/[^a-zA-Zа-яА-Я0-9\s]/.test(rawWord)){
                      for (let i = 1; i < rawWord.length; i++) {
                        if(/^[^a-zA-Zа-яА-Я0-9]+$/.test(rawWord.slice(0, i)))
                        {
                          leftIndex = i
                        } else {
                          break
                        }
                      }

                      for (let i = rawWord.length - 1; i >= 0 ; i--) {
                        if(/^[^а-яА-Я0-9]+$/.test(rawWord.slice(i, rawWord.length)))
                        {
                          rightIndex = i
                        } else {
                          break
                        }
                      }
                    }

                    console.log('FINAL REPORT')
                    if(!isSpelledWrong && isGrammaticallyWrong){
                      corrections = [grammarCorrections[tempIndex]]
                    }

                    return (
                      rawWord === ' '
                      ? <span style={{whiteSpace: 'nowrap'}}>&nbsp;</span>
                      : rawWord === 'PARAGPRAPH_SYMBOL'
                        ? <br />
                        : <span style={{whiteSpace: 'nowrap'}}>
                            {rawWord.slice(0, leftIndex) && (<span className={'littleSpanCorrect'}>
                              {rawWord.slice(0, leftIndex)}
                            </span>)}
                            {renderWord(isSpelledWrong, isGrammaticallyWrong, rawWord.slice(leftIndex, rightIndex), false, corrections, charIndex)}
                            {rawWord.slice(rightIndex) && (<span className={'littleSpanCorrect'}>
                              {rawWord.slice(rightIndex)}
                            </span>)}
                            &nbsp;
                          </span>
                          )})}
                                      
           </div>
              {/* {isErrorLoading || grammarsThinking != 0 && (
              <Spinner />)}    */}
          </div>
        </div>

        <div className="titleColumn" >
          <div className="titleBox">
            <p className="title">
              {style
              ? (
                  <>
                  {languageConstants.updatedTitle.slice(0, languageConstants.updatedTitle.search(/\{0\}/))}
                  <span className={styleTextStyleClass}>{styleText}</span>
                  {languageConstants.updatedTitle.slice(languageConstants.updatedTitle.search(/\{0\}/) + 3)}
                  </>
                )
              :
                languageConstants.initialTitle
              }
            </p>
            <div className="iconBox">
              <FontAwesomeIcon icon={styleIcon} size='6x' beat/>
            </div>
          </div>
          <div className="infoBox">
            <p style={{marginTop: 0}}>
                {languageConstants.wordCount}{rawText ? wordCount : 0}
            </p>
            {!isStyleLoading
            ? (<div className="buttonBox">
                <div className="checkButton" onClick={() => applySlovcho()}>
                  <p className="buttonText">
                    {style ? languageConstants.checkAgainButton: languageConstants.checkButton}
                  </p>
                </div>
              </div>)
            : (<div className="buttonBox">
                <div className="checkButtonLoading">
                    {<DotsBouncing />}
                </div>
              </div>)}
          </div>
        </div>
      </div>
    </div>
  );
}


export default App;














