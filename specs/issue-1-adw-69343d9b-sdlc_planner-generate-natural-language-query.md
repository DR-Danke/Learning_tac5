# Feature: Random Natural Language Query Generator

## Feature Description
Create a new button in the Natural Language SQL Interface that automatically generates interesting, contextually-aware natural language queries based on the existing database tables and their structure. When clicked, the button generates a random query (limited to two sentences maximum) and populates the query input field, allowing users to execute it manually. The button always overwrites the current content in the input field and is styled consistently with the "Upload Data" button, positioned with justify-apart spacing from the primary action buttons.

## User Story
As a user
I want a button that generates random natural language queries based on my database schema
So that I can explore my data with interesting query examples without having to think of questions myself

## Problem Statement
Users often struggle to come up with meaningful queries when first exploring their data, or may not fully understand what questions they can ask of their database. Having to manually type queries can be a barrier to discovering the full potential of the natural language SQL interface. New users especially benefit from seeing example queries that are contextually relevant to their actual data structure.

## Solution Statement
Implement a "Generate Query" button that leverages the existing `llm_processor.py` module to create intelligent, context-aware natural language queries based on the current database schema. The button will:
1. Analyze the available tables and their column structures
2. Use LLM capabilities to generate interesting, varied queries (e.g., aggregations, filters, joins)
3. Populate the query input field with the generated text
4. Always overwrite existing content in the field
5. Be styled consistently with the "Upload Data" button for visual harmony
6. Be positioned alongside primary buttons with proper spacing

## Relevant Files
Use these files to implement the feature:

- **app/server/server.py** (lines 1-280) - Main FastAPI server with API endpoints. We'll add a new `/api/generate-query` endpoint here that generates random queries based on database schema.

- **app/server/core/llm_processor.py** (lines 1-162) - Contains LLM integration with OpenAI and Anthropic APIs. We'll add a new function `generate_random_query()` that creates contextually-aware natural language queries based on table schemas.

- **app/server/core/data_models.py** (lines 1-82) - Pydantic models for API requests/responses. We'll add `GenerateQueryRequest` and `GenerateQueryResponse` models to support the new endpoint.

- **app/server/core/sql_processor.py** - Contains `get_database_schema()` function used to retrieve table information for query generation context.

- **app/client/index.html** (lines 1-99) - HTML structure of the application. We'll add a new "Generate Query" button in the query controls section alongside the existing "Query" and "Upload Data" buttons (line 22-26).

- **app/client/src/main.ts** (lines 1-423) - Main TypeScript application logic. We'll add a click handler for the new "Generate Query" button that calls the API and populates the query input field.

- **app/client/src/api/client.ts** - API client utilities. We'll add a new `generateQuery()` function to call the `/api/generate-query` endpoint.

- **app/client/src/types.d.ts** - TypeScript type definitions. We'll add type definitions for the generate query request/response.

- **app/client/src/style.css** - CSS styles. We'll ensure the new button follows the existing "Upload Data" button styling.

### New Files

- **.claude/commands/e2e/test_generate_query.md** - E2E test file to validate the random query generation feature works correctly. This test will verify that clicking the button generates a query, populates the input field, and the query can be executed successfully.

- **app/server/tests/core/test_query_generator.py** - Unit tests for the query generation logic, including tests for various table schemas, edge cases (empty database, single table, multiple tables), and LLM response handling.

## Implementation Plan

### Phase 1: Foundation
Create the backend infrastructure to support query generation. This includes:
- Adding new Pydantic models for the API request/response
- Creating the core query generation logic in `llm_processor.py`
- Setting up the FastAPI endpoint to handle query generation requests
- Adding unit tests to validate the query generation logic

### Phase 2: Core Implementation
Build the frontend interface and API integration:
- Add the "Generate Query" button to the HTML with appropriate styling
- Implement the TypeScript logic to call the API and populate the input field
- Add TypeScript type definitions for the new API
- Update the API client with the new endpoint function
- Ensure proper error handling and loading states

### Phase 3: Integration
Connect all components and validate the end-to-end functionality:
- Test the complete flow from button click to query population
- Create E2E tests to validate the feature works as expected
- Run all existing tests to ensure no regressions
- Validate frontend build and TypeScript compilation

## Step by Step Tasks

### Backend Data Models
- Add `GenerateQueryRequest` model to `app/server/core/data_models.py` with optional parameters for query complexity
- Add `GenerateQueryResponse` model with fields: `generated_query` (str), `schema_context` (optional str for debugging), and `error` (optional str)

### Backend Query Generation Logic
- Create `generate_random_query()` function in `app/server/core/llm_processor.py` that:
  - Takes database schema information as input
  - Constructs a prompt for the LLM to generate interesting queries
  - Includes instructions to limit output to two sentences maximum
  - Returns varied query types (aggregations, filters, joins, time-based queries, etc.)
  - Handles edge cases (empty database, single table, multiple tables)
- Use existing LLM routing logic (OpenAI/Anthropic) from `generate_sql()` function
- Implement proper error handling for LLM failures

### Backend API Endpoint
- Add `POST /api/generate-query` endpoint in `app/server/server.py`
- Use the `GenerateQueryRequest` and `GenerateQueryResponse` models
- Call `get_database_schema()` to get current table information
- Invoke `generate_random_query()` with schema context
- Return the generated query with proper error handling
- Add logging for successful query generation and failures

### Backend Unit Tests
- Create `app/server/tests/core/test_query_generator.py` with tests for:
  - Query generation with various table schemas (single table, multiple tables)
  - Query generation with different column types (numeric, text, date)
  - Edge case: empty database (should return helpful error message)
  - Edge case: tables with no rows
  - Query length validation (ensure ≤2 sentences)
  - LLM provider fallback logic
  - Error handling for LLM failures

### Frontend Type Definitions
- Add `GenerateQueryRequest` and `GenerateQueryResponse` interfaces to `app/client/src/types.d.ts`
- Ensure types match the backend Pydantic models exactly

### Frontend API Client
- Add `generateQuery()` function to `app/client/src/api/client.ts`
- Function should call `POST /api/generate-query` endpoint
- Return typed `GenerateQueryResponse`
- Include proper error handling

### Frontend UI - HTML Button
- Add "Generate Query" button in `app/client/index.html` within the `.query-controls` div (around line 22-26)
- Position it between the "Query" and "Upload Data" buttons
- Use class `secondary-button` to match "Upload Data" styling
- Add unique id `generate-query-button` for JavaScript targeting

### Frontend UI - TypeScript Logic
- Add `initializeGenerateQuery()` function in `app/client/src/main.ts`
- Implement click handler that:
  - Disables the button and shows loading state
  - Calls `api.generateQuery()`
  - Populates the query input field with the generated query (overwrites existing content)
  - Re-enables the button after completion
  - Displays error messages if generation fails
- Call `initializeGenerateQuery()` in the DOMContentLoaded event listener

### Frontend UI - Styling
- Review `app/client/src/style.css` to ensure `.secondary-button` class provides consistent styling
- Add any necessary CSS for the button spacing using flexbox justify-apart pattern
- Ensure button has proper hover and disabled states

### E2E Test Creation
- Create `.claude/commands/e2e/test_generate_query.md` following the pattern from `test_basic_query.md`
- Include test steps:
  1. Navigate to application
  2. Verify "Generate Query" button is visible
  3. Click "Generate Query" button
  4. Verify query input field is populated with text
  5. Verify text length is reasonable (≤2 sentences)
  6. Click "Query" button to execute the generated query
  7. Verify results appear (or graceful error if no tables exist)
  8. Take screenshots at each step
- Define success criteria:
  - Button is clickable and responsive
  - Query is generated and populates input field
  - Generated query is valid and executable
  - No JavaScript errors occur

### Run Validation Commands
- Execute all commands from the "Validation Commands" section below
- Fix any test failures or build errors
- Ensure zero regressions in existing functionality

## Testing Strategy

### Unit Tests
- **Query Generation Logic**: Test `generate_random_query()` with various schema configurations
  - Single table with simple columns
  - Multiple tables with relationships
  - Tables with different data types (integers, text, dates, booleans)
  - Edge case: no tables in database
  - Edge case: tables with zero rows
- **LLM Response Validation**: Test that generated queries meet the 2-sentence limit
- **Error Handling**: Test graceful failures when LLM APIs are unavailable
- **Provider Routing**: Test that both OpenAI and Anthropic providers work correctly

### Integration Tests
- **API Endpoint**: Test `/api/generate-query` returns valid responses
- **Schema Context**: Verify endpoint retrieves current database schema correctly
- **Error Responses**: Test endpoint returns appropriate errors when no tables exist

### E2E Tests
- **Button Interaction**: Verify button click triggers query generation
- **Field Population**: Verify generated query appears in input field
- **Query Execution**: Verify generated query can be successfully executed
- **Loading States**: Verify button shows loading state during generation
- **Error Display**: Verify error messages appear when generation fails

### Edge Cases
- **Empty Database**: User clicks generate button with no tables loaded - should show helpful error message
- **API Failures**: LLM API is unavailable or returns error - should show graceful error to user
- **Long Queries**: LLM generates query longer than 2 sentences - should be truncated or regenerated
- **Existing Query Text**: Input field has existing text - should be completely overwritten
- **Multiple Rapid Clicks**: User clicks generate button multiple times quickly - should handle gracefully with button disable state
- **No API Keys**: Neither OpenAI nor Anthropic keys are configured - should show appropriate error message

## Acceptance Criteria
- A "Generate Query" button exists in the query section, styled consistently with the "Upload Data" button
- Button is positioned with proper spacing (justify-apart) from other primary buttons
- Clicking the button generates a contextually-aware natural language query based on current database schema
- Generated queries are limited to a maximum of two sentences
- Generated query always overwrites any existing text in the query input field
- Button shows loading state during query generation
- Appropriate error messages are displayed if query generation fails (e.g., no tables, API error)
- Generated queries are varied and interesting (not always the same query)
- Generated queries can be successfully executed by clicking the "Query" button
- All existing functionality remains unchanged (no regressions)
- All existing tests pass
- New unit tests for query generation pass
- E2E test validates the complete feature workflow
- TypeScript compilation succeeds with no errors
- Frontend build completes successfully

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

Read `.claude/commands/test_e2e.md`, then read and execute the new E2E test file `.claude/commands/e2e/test_generate_query.md` to validate this functionality works.

- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/server && uv run pytest tests/core/test_query_generator.py -v` - Run specific query generator tests
- `cd app/client && bun tsc --noEmit` - Run frontend tests to validate the feature works with zero regressions
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions

## Notes

### LLM Prompt Design
The prompt for generating random queries should include:
- Clear instructions to generate diverse query types (aggregations, filters, joins, time-based)
- Strict 2-sentence maximum limit
- Request for queries that showcase the natural language capabilities
- Context about available tables and columns
- Examples of good queries: "Show me all users who signed up in the last month", "What is the average price of products by category?", "Count the number of events per user"

### Query Variety Strategies
To ensure queries are interesting and varied:
- Include randomization instructions in the LLM prompt
- Suggest different query patterns: aggregations (COUNT, AVG, SUM), filters (WHERE), sorting (ORDER BY), limits (TOP N), time-based (last week, this month), joins (when multiple tables exist)
- If only one table exists, focus on filters and aggregations
- If multiple tables exist, occasionally suggest joins

### API Key Handling
Follow the existing pattern in `llm_processor.py`:
- Check for OPENAI_API_KEY first (priority)
- Fall back to ANTHROPIC_API_KEY if OpenAI not available
- Return clear error message if neither key is configured

### Security Considerations
- Query generation does not execute SQL, only generates natural language text
- Validation happens when user manually clicks "Query" button
- No SQL injection concerns as the generated text goes through existing query processing pipeline
- Schema information exposed to LLM is already available through existing `/api/schema` endpoint

### Performance Considerations
- Query generation may take 1-3 seconds depending on LLM API response time
- Button should be disabled during generation to prevent multiple simultaneous requests
- Consider caching schema information to reduce database queries (optional optimization)

### Future Enhancements (Out of Scope)
- Add a history of generated queries
- Allow users to favorite generated queries
- Provide difficulty levels (simple, moderate, complex)
- Generate queries based on recent query patterns
- Support for query templates or categories
