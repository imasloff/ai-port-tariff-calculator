import os 
from loguru import logger
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.retrieval import get_retriever
from pydantic import BaseModel, Field


llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_retries=3,
)

class InputParameters(BaseModel):
    """Schema for extraction of the vessel information for calculation of port dues."""
    port_name: str = Field(description="The name of the port in which the vessel is berthing.", default="Durban")
    vessel_details: str = Field(
        description="The detailed extensive description of the vessel",
        examples=[
            """
            General
            Vessel Name: SUDESTADA
            Built: 2010
            Flag: MLT - Malta
            Classification Society: Registro Italiano Navale
            Call Sign: [Not provided]
            
            Main Details
            Lloyds / IMO No.: [Not provided]
            Type: Bulk Carrier
            DWT: 93,274
            GT / NT: 51,300 / 31,192
            LOA (m): 229.2
            Beam (m): 38
            Moulded Depth (m): 20.7
            LBP: 222
            Drafts SW S / W / T (m): 14.9 / 0 / 0
            Suez GT / NT: - / 49,069
            
            Communication
            E-mail: [Not provided]
            Commercial E-mail: [Not provided]
            
            DRY
            Number of Holds: 7
            
            Cargo Details
            Cargo Quantity: 40,000 MT
            Days Alongside: 3.39 days
            Arrival Time: 15 Nov 2024 10:12
            Departure Time: 22 Nov 2024 13:00
            
            Activity/Operations
            Activity: Exporting Iron Ore
            Number of Operations: 2
            """
        ],
        default="No vessel details provided.",
    )


def extract_input_parameters(text: str) -> InputParameters:
    """Extract the input parameters from the text."""
    extraction_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", 
            """
            You are an expert extraction algorithm.
            Only extract relevant information from the text.
            If you do not know the value of an attribute asked to extract,
            return null for the attribute's value.
            """),
            ("human", "{input}"),
        ]
    )
    extraction_llm = llm.with_structured_output(schema=InputParameters)
    extraction_chain = extraction_prompt | extraction_llm
    return extraction_chain.invoke({"input": text})

def build_query(tariff: str, port_name: str) -> str:
    """Build the query for the retrieval of the tariff document."""
    return f"{tariff}, {port_name}"

def retrieve_context(tariff: str, port_name: str) -> str:
    """Retrieve the context for the given query."""
    query = build_query(tariff, port_name)
    rerank, top_n, k, fetch_k = True, 35, 50, 70
    
    if tariff in ["light dues", "vehicle traffic services (VTS) dues"]:
        top_n = 25
    elif tariff == "port dues":
        top_n = 10
    elif tariff == "towage dues":
        top_n = 40
    elif tariff == "pilotage dues":
        top_n, k = 50, 70
    elif tariff == "running of vessel lines dues":
        top_n = 45

    kwargs = {"search_kwargs": {"k": k, "fetch_k": fetch_k}}
    logger.info(f"Retrieving context for {query} with top_n = {top_n} and {kwargs}")
    retriever = get_retriever(rerank=rerank, top_n=top_n, **kwargs)
    documents = retriever.invoke(query)
    return "\n\n".join([doc.page_content for doc in documents])

def calculate_tariff(
    tariff: str,
    port_name: str,
    vessel_details: str,
) -> str:
    """Calculate the tariff for the given vessel."""
    calculation_prompt_template = """
        You are an expert in South African port tariff calculations.
        Use the information provided in the Context to compute the exact amount of the **{tariff}** for the given vessel.

        You are given the following information:
        ### CONTEXT
        {context}

        Here is the information about the vessel berthing in the port of **{port_name}**:
        ### VESSEL DETAILS
        {vessel_details}

        Calculate ONLY the **{tariff}** for the given vessel using the information provided in the Context and the Vessel Details.

        ### INSTRUCTIONS
        - Analyze the Vessel Details and the Context carefully.
        - Pay a special attention to the cpecific rates.
        - DO NOT calculate any other dues or tariffs, only the **{tariff}**.
        - Extract specific rules for calculating the dues from the Context.
        - Use the extracted rules to compute the specific dues for the given vessel.
        
        ### OUTPUT
        - Provide ONLY the calculation breakdown and the final amount of **{tariff}** in South African Rand (ZAR).
    """
    calculation_prompt = ChatPromptTemplate.from_template(calculation_prompt_template)
    calculation_chain = {
        "tariff": lambda x: tariff,
        "context": lambda x: retrieve_context(tariff, x["port_name"]),
        "vessel_details": lambda x: x["vessel_details"],
        "port_name": lambda x: x["port_name"],
    } | calculation_prompt | llm | StrOutputParser()

    return calculation_chain.invoke({"port_name": port_name, "vessel_details": vessel_details})


def calculate_all_tariffs(input: str) -> str:
    """Calculate all tariffs for the given input."""
    input_parameters = extract_input_parameters(input)
    port_name = input_parameters.port_name
    vessel_details = input_parameters.vessel_details

    tariffs = [
        "light dues", 
        "port dues",
        "towage dues",
        "vehicle traffic services (VTS) dues",
        "pilotage dues",
        "running of vessel lines dues",
    ]

    results = []
    for tariff in tariffs:
        result = calculate_tariff(tariff, port_name, vessel_details)
        results.append(f"\n-------------------------------------\n## {tariff.upper()}:\n\n{result}\n-------------------------------------\n")

    return "\n\n".join(results)


if __name__ == "__main__":
    sample_input = """
        Calculate the different tariffs payable by the following vessel berthing at the port of Durban:\n
        Vessel Details:

        General
        Vessel Name: SUDESTADA
        Built: 2010
        Flag: MLT - Malta
        Classification Society: Registro Italiano Navale
        Call Sign: [Not provided]
        
        Main Details
        Lloyds / IMO No.: [Not provided]
        Type: Bulk Carrier
        DWT: 93,274
        GT / NT: 51,300 / 31,192
        LOA (m): 229.2
        Beam (m): 38
        Moulded Depth (m): 20.7
        LBP: 222
        Drafts SW S / W / T (m): 14.9 / 0 / 0
        Suez GT / NT: - / 49,069
        
        Communication
        E-mail: [Not provided]
        Commercial E-mail: [Not provided]
        
        DRY
        Number of Holds: 7
        
        Cargo Details
        Cargo Quantity: 40,000 MT
        Days Alongside: 3.39 days
        Arrival Time: 15 Nov 2024 10:12
        Departure Time: 22 Nov 2024 13:00
        
        Activity/Operations
        Activity: Exporting Iron Ore
        Number of Operations: 2
    """
    result = calculate_all_tariffs(sample_input)
    print(result)
    