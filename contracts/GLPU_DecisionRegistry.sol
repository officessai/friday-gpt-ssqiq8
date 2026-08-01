// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title GLPU_DecisionRegistry
 * @dev Rejestr decyzji podejmowanych przez silnik ∆Q8 i agentów HumanAI
 */
contract GLPU_DecisionRegistry {
    address public owner;

    enum Agent {
        Friday,
        Lyra,
        Echo
    }

    struct Decision {
        Agent agent;
        string action;
        uint256 timestamp;
        int256 sentimentScore;
        bool authorized;
    }

    mapping(uint256 => Decision) public decisions;
    uint256 public decisionCount;

    event DecisionLogged(uint256 id, Agent agent, string action, bool authorized);

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only GLPU Owner can authorize");
        _;
    }

    // Zapisywanie decyzji wygenerowanej przez Pythonowy silnik ∆Q8
    function logAIDecision(Agent _agent, string memory _action, int256 _sentiment) public onlyOwner {
        decisionCount++;
        decisions[decisionCount] = Decision({
            agent: _agent,
            action: _action,
            timestamp: block.timestamp,
            sentimentScore: _sentiment,
            authorized: true
        });

        emit DecisionLogged(decisionCount, _agent, _action, true);
    }
}
