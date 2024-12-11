export type AIModel = 'gpt-4' | 'gpt-3.5-turbo' | 'claude-3-opus' | 'claude-3-sonnet'

export interface AIConfig {
  model: AIModel
  maxTokens: number
  temperature: number
  topP: number
  systemPrompt?: string
}

export interface AIUsage {
  tokens: number
  cost: number
  timestamp: Date
}

export interface AIResponse {
  content: string
  usage: AIUsage
  model: AIModel
}

export type AIError =
  | 'RATE_LIMIT_EXCEEDED'
  | 'TOKEN_LIMIT_EXCEEDED'
  | 'INVALID_REQUEST'
  | 'SERVICE_UNAVAILABLE'