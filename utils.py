import requests
import time
import json

def start_orchestrator_job(token, question, organizationunitid, releasekey):
    headers = {
        'authorization': f'Bearer {token}',
        'x-uipath-organizationunitid': organizationunitid,
        'Content-Type': 'application/json',
    }

    json_data = {
        'startInfo': {
            'ReleaseKey': releasekey,
            'InputArguments': f'{{"query":"{question}"}}',
        },
    }
    response = requests.post(
        'https://staging.uipath.com/0093fb79-b0d8-4510-9baf-5c837ed017c4/snowflakehackweek2025/orchestrator_/odata/Jobs/UiPath.Server.Configuration.OData.StartJobs',
        headers=headers,
        json=json_data,
    )
    response.raise_for_status()

    return response.json().get('value')[0].get('Key')


def get_job_response(token, job_key, organizationunitid):
    headers = {
        'authorization': f'Bearer {token}',
        'x-uipath-organizationunitid': organizationunitid,
    }

    max_retries = 30
    retry_delay = 2

    while (max_retries > 0):
        response = requests.get(
            f'https://staging.uipath.com/0093fb79-b0d8-4510-9baf-5c837ed017c4/snowflakehackweek2025/orchestrator_/odata/Jobs/UiPath.Server.Configuration.OData.GetByKey(identifier={job_key})?$expand=Robot,Release,Machine',
            headers=headers,
        )
        response.raise_for_status()
        job_data = response.json()
        
        if job_data.get('State') != 'Successful':
            time.sleep(retry_delay)
            max_retries -= 1
        else:
            # Parse the OutputArguments JSON string
            output_args_str = job_data.get('OutputArguments')
            if output_args_str:
                try:
                    output_args = json.loads(output_args_str)
                    # Return the complete structured response
                    return {
                        'generatedSQLQuery': output_args.get('generatedSQLQuery'),
                        'queryExplanation': output_args.get('queryExplanation'),
                        'queryExecutionResults': output_args.get('queryExecutionResults')
                    }
                except json.JSONDecodeError as e:
                    print(f"Failed to parse OutputArguments JSON: {e}")
                    return output_args_str  # Return raw string if JSON parsing fails
            return None
        
    return ""
