export default function AuthenticationOutcome(inputMarketManagerName, inputOutcome)
{
    return {
        marketmanagername: inputMarketManagerName || "",
        outcome: inputOutcome || ""
    };
}