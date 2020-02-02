export default function StrategyInfo(inputCompilationResult, inputId, inputIsCompiled, inputLanguage)
{
    let formattedBool = (inputIsCompiled === undefined) ? undefined : inputIsCompiled.toString();

    return {
        compilationresult: inputCompilationResult || "",
        id: inputId || "",
        iscompiled: formattedBool || "",
        language: inputLanguage || ""      
    };
}