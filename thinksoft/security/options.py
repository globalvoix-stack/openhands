from thinksoft.security.analyzer import SecurityAnalyzer
from thinksoft.security.grayswan.analyzer import GraySwanAnalyzer
from thinksoft.security.invariant.analyzer import InvariantAnalyzer
from thinksoft.security.llm.analyzer import LLMRiskAnalyzer

SecurityAnalyzers: dict[str, type[SecurityAnalyzer]] = {
    'invariant': InvariantAnalyzer,
    'llm': LLMRiskAnalyzer,
    'grayswan': GraySwanAnalyzer,
}
