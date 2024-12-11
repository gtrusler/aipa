<!-- markdownlint-disable -->
# Next.js 14 SAAS Boilerplate with Supabase

A modern, production-ready boilerplate for SAAS applications built with Next.js 14, TypeScript, Supabase, OpenAI/Claude integration, and Cloudflare R2 storage.

## Features

- 🔐 Authentication with Supabase Auth
- 👤 User profile management
- 🛡️ Protected routes
- 🌤️ Weather & Air Quality Data
- 📰 News Integration
- 🎨 Tailwind CSS for styling
- 📝 TypeScript for type safety
- 🧪 ESLint + Prettier for code quality
- 🔄 Husky for pre-commit hooks
- 🤖 AI Integration (OpenAI & Claude)
- 📦 File Storage with Cloudflare R2
- 🚦 Rate Limiting
- 📊 Usage Tracking

### UI Components

This boilerplate uses [shadcn/ui](https://ui.shadcn.com/), a collection of re-usable components built using Radix UI and Tailwind CSS. These components are:

- Accessible
- Customizable
- Open Source
- Beautifully designed

#### Available Components

To add a shadcn/ui component to your project:

```bash
npx shadcn-ui@latest add [component-name]
```

For example, to add the button component:

```bash
npx shadcn-ui@latest add button
```

#### Styling

The project uses a custom theme configuration that includes both light and dark modes. The theme colors and other design tokens are defined in:

- `src/app/globals.css` - Global styles and CSS variables
- `tailwind.config.ts` - Tailwind configuration including theme extensions
- `src/lib/utils.ts` - Utility functions for styling

#### Dark Mode

Dark mode is supported out of the box using the `class` strategy. To toggle between light and dark mode, you can use the `useTheme` hook from `next-themes`.

### Weather Features

The application includes comprehensive weather and environmental data:

- Current weather conditions
- Air quality index and pollutants
- Pollen levels and allergy information
- Caching for optimal performance
- Error handling and fallback mechanisms

Example usage:

```typescript
import { WeatherClient } from '@/lib/weather/client'
import { AllergyClient } from '@/lib/weather/allergy'

// Get weather data
const weatherClient = new WeatherClient()
const conditions = await weatherClient.getCurrentConditions(location)

// Get air quality and pollen data
const allergyClient = new AllergyClient()
const airQuality = await allergyClient.getAirQuality(location)
const pollenLevels = await allergyClient.getPollenData(location)
```

### News Integration

The application fetches and displays news from multiple sources:

- Local Austin news from Fox 7
- National news from Fox News
- Customizable news categories
- Article summaries
- Relative timestamps
- Caching with TTL

Example usage:

```typescript
import { NewsClient } from '@/lib/news/client'

const newsClient = new NewsClient()

// Get news for specific category
const articles = await newsClient.getNews('austin', 3)

// Get news from multiple categories
const allNews = await newsClient.getMultipleCategories({
  categories: ['austin', 'latest', 'us', 'world'],
  limitPerCategory: 3
})
```

Available news categories:
- `austin`: Local Austin news
- `latest`: Breaking news
- `us`: National news
- `world`: International news
- `politics`: Political news
- `science`: Science and technology
- `health`: Health news
- `sports`: Sports news
- `travel`: Travel news
- `tech`: Technology news
- `opinion`: Opinion pieces

## Prerequisites

- Node.js 18.17 or later
- npm or yarn
- A Supabase account and project
- OpenAI API key
- Anthropic API key
- Cloudflare R2 credentials
- Redis instance (for rate limiting)

## Environment Variables

Create a `.env.local` file with the following variables:

```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# AI Configuration
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
AI_RATE_LIMIT_REQUESTS=100
AI_RATE_LIMIT_WINDOW_MS=60000
AI_MAX_TOKENS_PER_REQUEST=2000

# Weather & Air Quality
TOMORROW_API_KEY=your_tomorrow_api_key
BREEZOMETER_API_KEY=your_breezometer_key
WEATHER_CACHE_TTL=300
ALLERGY_CACHE_TTL=300

# News Configuration
NEWS_CACHE_TTL=300
NEWS_ARTICLES_PER_CATEGORY=3
DEFAULT_NEWS_CATEGORIES=austin,latest,us,world

# Cloudflare R2
R2_ACCOUNT_ID=your_account_id
R2_ACCESS_KEY_ID=your_access_key
R2_SECRET_ACCESS_KEY=your_secret_key
R2_BUCKET_NAME=your_bucket_name
R2_PUBLIC_URL=your_public_url

# Redis (for rate limiting)
REDIS_URL=your_redis_url
```

## Project Structure

```
├── src/
│   ├── app/                 # Next.js app router pages
│   ├── components/         # React components
│   │   ├── auth/          # Authentication components
│   │   └── ...
│   ├── lib/               # Library code
│   │   ├── supabase/     # Supabase client and utilities
│   │   ├── ai/           # AI integration utilities
│   │   ├── storage/      # R2 storage utilities
│   │   ├── weather/      # Weather and air quality services
│   │   ├── news/         # News feed integration
│   │   ├── context/      # Context management for LLM
│   │   └── utils/        # Common utilities and helpers
│   ├── hooks/            # Custom React hooks
│   ├── utils/            # Utility functions
│   ├── types/            # TypeScript type definitions
│   └── styles/           # CSS styles
├── public/               # Static files
├── scripts/             # Test and utility scripts
└── tests/               # Test files
```

## AI Integration

The boilerplate includes integrations with both OpenAI and Anthropic:

- Rate limiting for API calls
- Token usage tracking
- Cost calculation
- Error handling
- Fallback mechanisms
- Type-safe responses

Example usage:

```typescript
import { generateOpenAIResponse } from '@/lib/ai/openai'
import { generateClaudeResponse } from '@/lib/ai/anthropic'

// Using OpenAI
const openAIResponse = await generateOpenAIResponse('Your prompt here')

// Using Claude
const claudeResponse = await generateClaudeResponse('Your prompt here')
```

## File Storage

Cloudflare R2 integration includes:

- Secure file uploads
- Type validation
- Size limits
- Image optimization
- Secure URL generation

Example usage:

```typescript
import { useFileUpload } from '@/hooks/useFileUpload'

const { upload, uploading, error } = useFileUpload()

const handleUpload = async (file: File) => {
  const config = {
    maxSizeMB: 10,
    allowedTypes: ['image/jpeg', 'image/png'],
    generateThumbnail: true
  }
  
  const result = await upload(file, userId, config)
}
```

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run format` - Format code with Prettier
- `npm run type-check` - Run TypeScript type checking

### Adding New Features

1. **AI Integration**
   - Add new models in `src/types/ai.ts`
   - Implement new providers in `src/lib/ai/`
   - Update cost calculations as needed

2. **Storage Features**
   - Add new storage utilities in `src/lib/storage/`
   - Update file validation in storage utilities
   - Add new file processing features as needed

## Security Considerations

- Environment variables are properly configured
- Rate limiting is implemented for AI endpoints
- File validation is enforced
- Secure URL generation for stored files
- Protected routes are properly secured
- Authentication state is handled securely

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

# Documentation

Visit our comprehensive documentation at [docs.your-domain.com](https://docs.your-domain.com) for:

- 📚 Getting Started Guide
- 🏗️ Architecture Overview
- 🔧 API Reference
- 📦 Component Documentation
- 🚀 Deployment Guide
- 💡 Examples & Tutorials

## Quick Links

- [Getting Started](https://docs.your-domain.com/getting-started)
- [API Reference](https://docs.your-domain.com/api-reference)
- [Deployment Guide](https://docs.your-domain.com/deployment)
- [Examples](https://docs.your-domain.com/examples)
